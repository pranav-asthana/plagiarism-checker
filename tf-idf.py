import os
import math
from nltk.tokenize import word_tokenize
from progressbar import ProgressBar
from pprint import pprint

def tf_idf_dict(document, corpus):
    N = len(corpus)
    dictionary = {}
    for term in document:
        term_frequency = math.log(document.count(term), 10)
        document_frequency = 0
        for doc in corpus:
            if term in doc:
                document_frequency += 1
        inverse_document_frequency = math.log(N / document_frequency, 10)
        tf_idf = term_frequency * inverse_document_frequency
        dictionary[term] = tf_idf
    return dictionary

corpus = []
pbar = ProgressBar()
for document in pbar(os.listdir('data')):
    # print('reading ', document)
    text = open(os.path.join('data', document), encoding = 'ISO-8859-1').read()
    text = word_tokenize(text)
    corpus.append(text)

for document in corpus:
    pprint(list(tf_idf_dict(document, corpus).values()))
