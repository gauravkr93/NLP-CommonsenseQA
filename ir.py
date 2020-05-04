# Adapted from https://github.com/ari9dam/McQueen/blob/master/scripts/Physical/ir_from_aristo.py

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q, Search
import csv
import json
import sys
from tqdm import tqdm 


class TextSearchSolver():
    """
    runs a query against elasticsearch and sums up the top `topn` scores. by default,
    `topn` is 1, which means it just returns the top score, which is the same behavior as the
    scala solver
    """
    def __init__(self,                   # pylint: disable=too-many-arguments
                 host: str="localhost",
                 port: int=9200,
                 index_name: str="cqa_kb2",
                 field_name: str="body",
                 topn: int=50) -> None:   # changed to 50 from 100
        self.client = Elasticsearch([host], port=port)
        #print(self.client)
        self.fields = [field_name]
        self.index_name = index_name
        self.topn = topn

    def score(self, question_stem: str, choice_text: str) -> float:
        """get the score from elasticsearch"""
        query_text = "{0} {1}".format(question_stem, choice_text)
        query = Q('multi_match', query=query_text, fields=self.fields)
        search = Search(using=self.client, index=self.index_name).query(query)[:self.topn]
        response = search.execute()
        return sum(hit.meta.score for hit in response)

    def search(self, query: str) -> list:
        """get the score from elasticsearch"""
        query_text = query
        query = Q('multi_match', query=query_text, fields=self.fields)
        #print (query)
        search = Search(using=self.client, index=self.index_name).query(query)[:self.topn]
        response = search.execute()
        #print(response)
        return [(hit.body.replace('\t', ' '),hit.meta.score) for hit in response]




if __name__ == "__main__":
    solver = TextSearchSolver()  # pylint: disable=invalid-name
    # print(solver.search("pulled up a chair but  was broken so  had to stand"))

    inpfile = sys.argv[1]
    in_fname, _ = inpfile.rsplit('_', 1)
    outfile = in_fname + "_IR.tsv"

    delimiter = "\t"

    all_results = {}
    with open(inpfile,'r') as tsvin, open(outfile, 'w') as csvout:
        tsvin = csv.reader(tsvin, delimiter=delimiter)
        csvout = csv.writer(csvout,delimiter=delimiter)
        for row in tqdm(tsvin,desc="Running IR:"):
            searchQuery = row[-1]
            out = solver.search(searchQuery)
            row.append(out)
            all_results[row[0]]=out
            csvout.writerow(row)
            # import pdb; pdb.set_trace()
            # print(str(i))

    import pickle
    with open(outfile+".pickled", 'wb') as handle:
        pickle.dump(all_results, handle, protocol=pickle.HIGHEST_PROTOCOL)