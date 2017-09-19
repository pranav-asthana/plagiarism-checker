import os
import math
import operator
import string
import nltk
from nltk.tokenize import wordpunct_tokenize
from progressbar import ProgressBar
from pprint import pprint
import matplotlib.pyplot as plt

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
        term_frequency = (1 + math.log(document.count(term), 10) if document.count(term) else 0)
        tf_vector.append(term_frequency)
    vect = list(map(operator.mul, tf_vector, idf_vector))
    return vect

def cosine_similarity(vector1, vector2):
    def norm(vector):
        return math.sqrt(sum(i**2 for i in vector))
    return sum(map(operator.mul, vector1, vector2)) / (norm(vector1) * norm(vector2))

corpus = []
vocabulary = []
pbar = ProgressBar()
print('Preparing data ...')
for document in pbar(os.listdir('data')):
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

print('Building similarity matrix ...')
sim_matrix = []
pbar = ProgressBar()
for document1 in pbar(tf_idf_matrix):
    sim_matrix.append([])
    for document2 in tf_idf_matrix:
        sim = cosine_similarity(document1, document2)
        sim_matrix[-1].append(sim)

for i in range(len(sim_matrix)):
    for j in range(len(sim_matrix[0])):
        if sim_matrix[i][j] > 0.9 and i < j:
            print(i, j)

plt.imshow(sim_matrix, cmap = 'gray')
plt.show()
