import math
import data_manager


class BoW:

    def __init__(self):
        self.bag = {}
        self.priors = []
        self.word_count = 0
        self.n_gram = 1

    def train(self, dataset=None, n_gram=1):
        """
        Train the model.
        :param dataset: 2D array of strings
        :param n_gram: N-gram value
        :return: returns bag
        """
        self.n_gram = n_gram

        dataset = dataset or []

        # Loop through the dataset
        for i in range(len(dataset)):

            data = dataset[i]
            # update total word count
            self.word_count += len(data.split(' '))

            data = list(filter(None, data.split(' ')))

            for j in range(len(data) - (n_gram - 1)):
                # loop through the data
                if n_gram != 1:
                    # if bigram or trigram
                    condition = ' '.join(data[j:j + n_gram - 1])
                    word = data[j + n_gram - 1]
                else:
                    # if unigram
                    condition = data[j + n_gram - 1]
                    word = None
                self._construct(word, condition)

        return self.bag

    def _construct(self, word, condition):

        bag = self.bag

        # If not in bag, create a new entry
        if condition not in bag:
            bag[condition] = {}
            bag[condition]['count'] = 0
            bag[condition]['next'] = {}
        # update the next dictionary
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
            condition = ' '.join(data[i:i + self.n_gram - 1])
            phrase = ''.join(data[i + self.n_gram - 1])

            # if condition isn't in bag
            if condition not in self.bag:
                # phrase count, condition count
                p_count = 0
                c_count = 0
            else:
                p_count = self.bag[condition]['count']
                # if the current word does not appear after condition
                if phrase not in self.bag[condition]['next']:
                    c_count = 0
                else:
                    c_count = self.bag[condition]['next'][phrase]
            # update the probability
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
            # if bi or trigram
            while current_words < max_words:
                random_number = random()
                current = ' '.join(essay.split()[(-self.n_gram + 1):])
                # scale probabilities between 0-1
                scaled_probabilities = self.scale_to_one(self.bag[current]['next'].values())
                # pick a word from the vocabulary
                i = self._pick(random_number, scaled_probabilities)
                next_word = list(self.bag[current]['next'].keys())[i]
                # add word to essay
                essay += ' ' + next_word
                next_word = ' ' + next_word + ' '
                # check whether punctuation or token
                if next_word != data_manager.start_token and next_word != data_manager.end_token \
                        and next_word not in data_manager.punctuations:
                    current_words += 1
        else:
            while current_words < max_words:
                # if unigram
                random_number = random()
                # scale probabilities between 0-1
                scaled_probabilities = self.scale_to_one([self.bag[x]['count'] for x in self.bag])
                # pick a word from the vocabulary
                i = self._pick(random_number, scaled_probabilities)
                next_word = list(self.bag.keys())[i]
                # add word to essay
                essay += ' ' + next_word
                # check whether punctuation
                if next_word not in data_manager.punctuations:
                    current_words += 1
        # remove tokens from the essay
        essay = essay.replace(data_manager.start_token.split()[0], '')
        essay = essay.replace(data_manager.end_token.split()[0], '')
        return ' '.join(essay.split())

    def perplexity(self, probability):
        return math.pow(2.0, -probability / len(self.bag.keys()))

    def save(self, path='./', name='model'):

        import pickle
        full_path = path + name
        with open(full_path, 'wb') as handle:
            pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(path='./', name='model'):

        import pickle

        full_path = path + name
        with open(full_path, 'rb') as handle:
            return pickle.load(handle)
