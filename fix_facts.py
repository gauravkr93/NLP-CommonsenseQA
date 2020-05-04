# Some knowledge sentences have unescaped quotes and unicode characters which are making ast.eval fail.

import pickle
import csv, sys, re
from tqdm import tqdm 

inpfile = sys.argv[1]
in_fname, _ = inpfile.rsplit('_', 1)
all_results = pickle.load( open(in_fname + "_IR.tsv.pickled", "rb" ) )

for k, facts in all_results.items():
    all_results[k] = [(re.sub(r"[^a-zA-Z0-9\.,']", " ", f.encode('ascii', errors='ignore').decode()).strip(), s) for f,s in facts]

delimiter = "\t"
with open(inpfile, 'r') as tsvin, open(in_fname + "_IR2.tsv", 'w') as csvout:
    tsvin = csv.reader(tsvin, delimiter=delimiter)
    tsvout = csv.writer(csvout,delimiter=delimiter)
    for row in tqdm(tsvin, desc="Fixing facts:"):
        # row[-1] = all_results[row[0]]
        row.append(all_results[row[0]])
        tsvout.writerow(row)