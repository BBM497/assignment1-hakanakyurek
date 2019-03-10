from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import math
from nltk.stem import LancasterStemmer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


class BoW:

    def __init__(self):
        self.bag = {}
        self.priors = []
        self.word_count = []

        self.start_token = '<s>'
        self.end_token = '</s>'

        self.stemmer = LancasterStemmer()

    def pre_process(self, dataset):

        # Apply stopword removal
        dataset = self.filter_stopwords(dataset)

        temp_dataset = []

        for data in dataset:
            temp_data = []
            for word in data.split(" "):
                # Apply stem if initialized
                temp_data.append(self.stemmer.stem(word))
            temp_dataset.append(temp_data)

        return temp_dataset

    def bow_unigram(self, labels, dataset=None):
        '''
        :param labels: label array for the dataset, each element should be Label enum type.
        :param dataset: 2D array of strings
        :return: returns bag
        '''
        dataset = dataset or []
        unique_label_count = len(set(labels))
        self.word_count = [0] * unique_label_count

        # Loop through the data
        for i in range(len(dataset)):

            data = dataset[i]
            label = labels[i].value

            self.word_count[label] += len(data.split(' '))

            for word in data.split(' '):
                self.construct(word, label, unique_label_count)

        return self.bag

    def construct(self, word, label, unique_label_count):
        # If not in BoW, add it to it
        if word not in self.bag:
            self.bag[word] = {k: 0 for k in range(unique_label_count)}
        # Increase frequency
        self.bag[word][label] += 1

    def set_priors(self):

        self.priors = [0] * len(self.word_count)

        for i in self.word_count:
            wc = self.word_count[i]
            self.priors[i] = wc / sum(self.word_count)

    # High complexity to make it modular
    def filter_stopwords(self, dataset):

        temp_dataset = []

        for data in dataset:

            temp = data.split(" ")

            for word in data.split(" "):
                # if word is a stopword
                if word in ENGLISH_STOP_WORDS:
                    # remove it
                    temp.remove(word)

            temp_dataset.append(' '.join(temp))

        return temp_dataset
