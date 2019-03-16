import math


class BoW:

    def __init__(self):
        self.bag = {}
        self.priors = []
        self.word_count = []
        self.n_gram = 1

    def __str__(self, *args, **kwargs):
        print("BoW model: n-gram:%, unique words in the bag:%".format(self.n_gram, len(self.bag.keys())))

    def train(self, labels, dataset=None, n_gram=1):
        """
        Train the model.
        :param labels: label array for the dataset, each element should be Label enum type.
        :param dataset: 2D array of strings
        :param n_gram: N-gram value
        :return: returns bag
        """
        self.n_gram = n_gram

        dataset = dataset or []
        unique_label_count = len(set(labels))
        self.word_count = [0] * unique_label_count

        # Loop through the data
        for i in range(len(dataset)):

            data = dataset[i]
            label = labels[i].value

            self.word_count[label] += len(data.split(' '))

            data = list(filter(None, data.split(' ')))

            for j in range(len(data) - (n_gram - 1)):
                if n_gram != 1:
                    condition = ' '.join(data[j:j + n_gram - 1])
                    word = data[j + n_gram - 1]
                else:
                    condition = data[j + n_gram - 1]
                    word = None
                self._construct(word, condition, label, unique_label_count)

        return self.bag

    def _construct(self, word, condition, label, unique_label_count):

        bag = self.bag

        # If not in BoW, add it to it
        if condition not in bag:
            bag[condition] = {k: 0 for k in range(unique_label_count)}
            bag[condition]['next'] = {}

        if word is not None:
            if word not in bag[condition]['next']:
                bag[condition]['next'][word] = 0
            else:
                bag[condition]['next'][word] += 1

        # Increase frequency
        bag[condition][label] += 1

    def set_priors(self):

        self.priors = [0] * len(self.word_count)

        for i in self.word_count:
            wc = self.word_count[i]
            self.priors[i] = wc / sum(self.word_count)

    def probability(self, numerator, denominator):
        probability = math.log2((numerator + 1) / (denominator + len(self.bag.keys())))
        return probability
