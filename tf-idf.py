import os
import math
import operator
import string
import nltk
from nltk.tokenize import wordpunct_tokenize
from progressbar import ProgressBar
from pprint import pprint

def get_idf_vector(corpus, vocabulary):
    N = len(corpus)
    idf_vector = []
    for term in vocabulary:
        document_frequency = 0
        for doc in corpus:
            if term in doc:
                document_frequency += 1
        inverse_document_frequency = math.log(N / document_frequency, 10)
        idf_vector.append(inverse_document_frequency)
    return idf_vector

def get_tf_idf_vector(document, idf_vector, vocabulary):
    vect = []
    tf_vector = []
    for term in vocabulary:
        try:
            term_frequency = 1 + math.log(document.count(term), 10)
        except:
            term_frequency = 0
        tf_vector.append(term_frequency)
    vect = list(map(operator.mul, tf_vector, idf_vector))
    return vect

corpus = []
vocabulary = []
pbar = ProgressBar()
print('Preparing data ...')
for document in (os.listdir('data')):
    # print('reading ', document)
    text = open(os.path.join('data', document), encoding = 'ISO-8859-1').read()
    text = wordpunct_tokenize(text)
    text = [word for word in text if word not in string.punctuation] # remove punctuation
    text = [word.lower() for word in text] # case folding
    text = [word for word in text if word not in nltk.corpus.stopwords.words('english')] # remove stopwords
    text = [nltk.stem.PorterStemmer().stem(word) for word in text] # stemming
    vocabulary.extend(text)
    corpus.append(text)
vocabulary = list(set(vocabulary))

idf_vector = get_idf_vector(corpus, vocabulary)

tf_idf_matrix = []

print('Building tf-idf matrix ...')
pbar = ProgressBar()
for document in pbar(corpus):
    tf_idf_vector = get_tf_idf_vector(document, idf_vector, vocabulary)
    tf_idf_matrix.append(tf_idf_vector)
