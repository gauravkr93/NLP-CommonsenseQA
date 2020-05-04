# Adapted from https://github.com/ari9dam/McQueen/blob/master/scripts/Physical/preIR.py

import pandas as pd
import os
import json
import numpy as np
import csv
import sys
from tqdm import tqdm


import nltk
nltk.download("stopwords")
nltk.download("punkt")


from stop_words import get_stop_words
from nltk.corpus import stopwords
import string


stop_words = set(get_stop_words('en'))         #About 900 stopwords
nltk_words = set(stopwords.words('english')) #About 150 stopwords
stop_words = stop_words.union(nltk_words)

def remove_stopwords(sent):
    sent = sent.lower().split(" ")
    s = " ".join(dict([(w, w) for w in sent if not w in stop_words]).keys())  # dicts are ordered in Python 3.6
    s = s.translate(str.maketrans('', '', string.punctuation))
    return s


def createIRFile(inpFile, outFile):
    choice_chars = ['A', 'B', 'C', 'D', 'E']
    with open(inpFile,'r') as jsonlin, open(outFile, 'w') as tsvout:
        # write the header
        # tsvout.write('id\tquestion\tanswer\tchoice\tquery\n')
        for line in jsonlin:
            tsvlines = []
            q = json.loads(line)
            l = [q['id'], q['question']['stem'].replace('\t', ' ')]
            l.append(str(ord(q['answerKey']) - ord('A')))

            choices_dict = {}
            for c in q['question']['choices']:
                choices_dict[c['label']] = c['text'].replace('\t', ' ')
            # To make sure TSV has choices in the order A,B,C,D,E
            l.append('dummy-choice')
            l.append('dummy-query')
            for i, c in enumerate(choice_chars):
                l[0] = f"{q['id']}:{i}"
                l[-2] = choices_dict[c]
                l[-1] = remove_stopwords(l[1] + ' ' + choices_dict[c])  # concat question and answer option
                tsvlines.append('\t'.join(l))
            
            tsvout.write('\n'.join(tsvlines))  # write out lines for each of the answer option query
            tsvout.write('\n')


if __name__ == "__main__":
    in_fname, in_ext = sys.argv[1].rsplit('.', 1)
    createIRFile(sys.argv[1], in_fname+'_preIR.tsv')