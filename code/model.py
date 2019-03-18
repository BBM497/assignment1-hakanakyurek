import math
import data_manager


class BoW:

    def __init__(self):
        self.bag = {}
        self.priors = []
        self.word_count = 0
        self.n_gram = 1

    def __str__(self, *args, **kwargs):
        print("BoW model: n-gram: {}, unique words in the bag: {}".format(self.n_gram, len(self.bag.keys())))

    def train(self, dataset=None, n_gram=1):
        """
        Train the model.
        :param dataset: 2D array of strings
        :param n_gram: N-gram value
        :return: returns bag
        """
        self.n_gram = n_gram

        dataset = dataset or []

        # Loop through the data
        for i in range(len(dataset)):

            data = dataset[i]

            self.word_count += len(data.split(' '))

            data = list(filter(None, data.split(' ')))

            for j in range(len(data) - (n_gram - 1)):
                if n_gram != 1:
                    condition = ' '.join(data[j:j + n_gram - 1])
                    word = data[j + n_gram - 1]
                else:
                    condition = data[j + n_gram - 1]
                    word = None
                self._construct(word, condition)

        return self.bag

    def _construct(self, word, condition):

        bag = self.bag

        # If not in BoW, add it to it
        if condition not in bag:
            bag[condition] = {}
            bag[condition]['count'] = 0
            bag[condition]['next'] = {}

        if word is not None:
            if word not in bag[condition]['next']:
                bag[condition]['next'][word] = 1
            else:
                bag[condition]['next'][word] += 1

        # Increase frequency
        bag[condition]['count'] += 1

    def probability(self, numerator, denominator):
        probability = math.log10((numerator + 1) / (denominator + len(self.bag.keys())))
        return probability

    def predict(self, data):
        data = data.split()
        probability_of_doc = 0

        for i in range(len(data) - (self.n_gram - 1)):
            phrase = ' '.join(data[i:i + self.n_gram - 1])
            condition = ''.join(data[i + self.n_gram - 1])

            if phrase not in self.bag:
                p_count = 0
                c_count = 0
            else:
                p_count = self.bag[phrase]['count']
                if condition not in self.bag[phrase]['next']:
                    c_count = 0
                else:
                    c_count = self.bag[phrase]['next'][condition]

            if condition is ' ':
                probability_of_doc += self.probability(p_count, len(self.bag.keys()))
            else:
                probability_of_doc += self.probability(p_count, c_count)

        return probability_of_doc

    def test(self, dataset):

        predictions = []
        for data in dataset:
            predictions.append(self.predict(data))

        return predictions

    @staticmethod
    def scale_to_one(list_of_smt):
        return [x/sum(list_of_smt) for x in list_of_smt]

    @staticmethod
    def _pick(random_number, list_of_smt):
        temp, i = 0, 0
        while temp < random_number:
            temp += list_of_smt[i]
            i += 1

        return i - 1

    def generate(self, max_words=30):

        from random import random

        essay = (self.n_gram - 1) * data_manager.start_token
        current_words = 0
        if self.n_gram > 1:
            while current_words < max_words:
                random_number = random()
                current = ' '.join(essay.split()[(-self.n_gram + 1):])

                scaled_probabilities = self.scale_to_one(self.bag[current]['next'].values())

                i = self._pick(random_number, scaled_probabilities)
                next_word = list(self.bag[current]['next'].keys())[i]

                essay += ' ' + next_word
                next_word = ' ' + next_word + ' '
                if next_word != data_manager.start_token and next_word != data_manager.end_token \
                        and next_word not in data_manager.punctuations:
                    current_words += 1
        else:
            while current_words < max_words:
                random_number = random()

                scaled_probabilities = self.scale_to_one([self.bag[x]['count'] for x in self.bag])

                i = self._pick(random_number, scaled_probabilities)
                next_word = list(self.bag.keys())[i]

                essay += ' ' + next_word
                if next_word not in data_manager.punctuations:
                    current_words += 1

        return essay