import os
import math
import operator
import string
import nltk
import re
import argparse
import itertools
import pickle
from nltk.tokenize import wordpunct_tokenize, sent_tokenize
from progressbar import ProgressBar
from pprint import pprint
import matplotlib.pyplot as plt

corpus, vocabulary, idf_vector = [None, None, None]

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

def segment_document(document_path):
    text = open(document_path, encoding = 'ISO-8859-1').read()
    text = ' '.join(text.split('\n'))
    sentence_list = sent_tokenize(text)
    j = 0
    i = 0
    segments = []
    while j < len(sentence_list):
        segmented_text = ' '. join(sentence_list[j:j+5])
        j += 5
        new_file = '.'.join(document_path.split('/')[-1].split('.')[:-1]) + '_' + str(i) + '.txt'
        segments.append([new_file, segmented_text])
        i += 1
    return segments

def get_tokens(text):
    text = wordpunct_tokenize(text)
    text = [word for word in text if word not in string.punctuation] # remove punctuation
    text = [word.lower() for word in text] # case folding
    text = [word for word in text if word not in nltk.corpus.stopwords.words('english')] # remove stopwords
    text = [nltk.stem.PorterStemmer().stem(word) for word in text] # stemming
    return text

def prepare_data(data_dir):
    corpus = []
    vocabulary = []
    pbar = ProgressBar()
    for document in pbar(os.listdir(data_dir)):
        # print('reading ', document)
        text = open(os.path.join(data_dir, document), encoding = 'ISO-8859-1').read()
        text = get_tokens(text)
        vocabulary.extend(text)
        corpus.append([document, text])
    vocabulary = list(set(vocabulary))
    return corpus, vocabulary

def main():
    parser = argparse.ArgumentParser(
                description='Compare a document with the corpus')
    parser.add_argument('corpus_path', type=str,
                        help='Path to corpus')
    parser.add_argument('text_path', type=str,
                        help='Path to text file for checking')
    parser.add_argument('-p', '--preprocess', dest='preprocess', action='store_true',
                        help='Preprocess the corpus')
    args = parser.parse_args()
    data_dir = args.corpus_path
    target_file = args.text_path

    if args.preprocess:
        print('Preparing data ...')
        new_dir = 'split_data'
        for document in os.listdir(data_dir):
            if new_dir not in os.listdir():
                os.mkdir(new_dir)
            segments = segment_document(os.path.join(data_dir, document))
            for segment in segments:
                open(os.path.join(new_dir, segment[0]), 'w', encoding = 'ISO-8859-1').write(segment[1])

        corpus, vocabulary = prepare_data(new_dir)

        idf_vector = get_idf_vector([document[1] for document in corpus], vocabulary)
        preprocessed = open('preprocessed', 'wb')
        pickle.dump([corpus, vocabulary, idf_vector], preprocessed)

    try:
        preprocessed = open('preprocessed', 'rb')
        corpus, vocabulary, idf_vector = pickle.load(preprocessed)
    except:
        print('Processed corpus not found')

    if corpus == None:
        print('Please pre-process the data first')
        return

    tf_idf_matrix = []

    print('Building tf-idf matrix ...')
    pbar = ProgressBar()
    for document in pbar(corpus):
        tf_idf_vector = get_tf_idf_vector(document[1], idf_vector, vocabulary)
        tf_idf_matrix.append([document[0], tf_idf_vector])

    print('Reading input file ...')
    scores = [['', 0]] * len(corpus)
    target_text = open(target_file, encoding = 'ISO-8859-1').read()
    segments = segment_document(target_file)
    pbar = ProgressBar()
    for segment in pbar(segments):
        target_text = get_tokens(segment[1])
        target_tf_idf = get_tf_idf_vector(target_text, idf_vector, vocabulary)

        index = 0
        for doc in tf_idf_matrix:
            sim = cosine_similarity(target_tf_idf, doc[1])
            # print('Accessing scores() ', index, ' with values ', doc[0], sim)
            scores[index] = [doc[0], scores[index][1] + sim]
            index += 1

    max_score = max([score[1] for score in scores])
    scores = [(score[0][:10], score[1]/max_score) for score in scores]
    scores1 = [score for score in scores if score[1] > 0.8]
    scores = {a: [q[1] for q in b] for a, b in itertools.groupby(sorted(scores), operator.itemgetter(0))}
    scores = list({a: sum(b) for a, b in scores.items()}.items())
    scores = sorted(scores, key = operator.itemgetter(1))
    scores = [(score[0], score[1]/max(scores, key = operator.itemgetter(1))[1]) for score in scores][-11:-1]
    results = open('results', 'wb')
    pickle.dump(scores, results)
    pprint(scores)

    # print('Building similarity matrix ...')
    # sim_matrix = []
    # pbar = ProgressBar()
    # for document1 in pbar(tf_idf_matrix):
    #     sim_matrix.append([])
    #     for document2 in tf_idf_matrix:
    #         sim = cosine_similarity(document1[1], document2[1])
    #         sim_matrix[-1].append(sim)
    #
    # # for i in range(len(sim_matrix)):
    # #     for j in range(len(sim_matrix[0])):
    # #         if sim_matrix[i][j] > 0.9 and i < j:
    # #             print(corpus[i][0], corpus[j][0])
    # output = [(corpus[i][0], corpus[j][0]) for i in range(len(sim_matrix[0])) for j in range(len(sim_matrix)) if sim_matrix[i][j] > 0.9 and i < j]
    # pprint([names for names in output if 'orig' in names[0] or 'orig' in names[1]])

    # plt.imshow(sim_matrix, cmap = 'gray')
    # plt.show()

if __name__ == '__main__':
    main()
