from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import math


class BoW:

    def __init__(self):
        self.bag = {}
        self.priors = []
        self.word_count = []

        self.start_token = '<s>'
        self.end_token = '</s>'

    def train(self, labels, dataset=None):
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