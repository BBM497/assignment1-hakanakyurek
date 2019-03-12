import os
import enum

start_token = ' _START_ '
end_token = ' _END_ '

punctuations = {'!': '!',
                '"': '"',
                '&': '&',
                ',': ',',
                '.': '.',
                ':': ':',
                ';': ';',
                '?': '?',
                '[': '[',
                ']': ']',
                ')': '(',
                '(': ')',
                '{': '{',
                '}': '}',
                }


class Label(enum.Enum):
    HAMILTON = 0
    MADISON = 1


def read(path=''):
    train_dataset = []
    train_labels = []
    test_dataset = []
    test_labels = []

    train_path = path + 'Train/'
    for file in os.listdir(train_path):

        file = open(train_path + file, 'r')
        lines = file.readlines()

        train_labels.append(Label.HAMILTON if lines[0] == 'HAMILTON \n' else Label.MADISON)
        train_dataset.append(lines[1])

        file.close()

    test_path = path + 'Test/'
    for file in os.listdir(test_path):

        file = open(test_path + file, 'r')
        lines = file.readlines()

        test_labels.append(Label.HAMILTON if lines[0] == 'HAMILTON \n' else Label.MADISON)
        test_dataset.append(lines[1])

        file.close()

    return train_dataset, train_labels, test_dataset, test_labels


def pre_process(dataset, n_gram=1):
    """
    Applies preprocessing to the dataset: stopword removal, stemming, and lowercase.
    :param dataset: 2D array of string
    :param n_gram: N-gram value
    :return: preprocessed dataset
    """

    x = (n_gram - 1)

    for i in range(len(dataset)):
        dataset[i] = dataset[i].lower()

    dataset = filter_stopwords(dataset)
    dataset = filter_punctuation(dataset, x)

    for i in range(len(dataset)):
        dataset[i] = start_token * x + dataset[i] + end_token * x

    return dataset


def filter_stopwords(dataset):
    """
    Filter stopwords in the given dataset.
    :param dataset: 2D array of string
    :return: return the filtered dataset
    """
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
    temp_dataset = []

    for data in dataset:

        temp = data.split(' ')

        for word in data.split(' '):
            # if word is a stopword
            if word in ENGLISH_STOP_WORDS:
                # remove it
                temp.remove(word)

        temp_dataset.append(' '.join(temp))

    return temp_dataset


def filter_punctuation(dataset, x):

    if x != 0:
        for key in punctuations.keys(): punctuations[key] = x * start_token + punctuations[key] + x * end_token
    else:
        for key in punctuations.keys(): punctuations[key] = ' ' + punctuations[key]

    trantab = str.maketrans(punctuations)
    for i in range(len(dataset)):

        dataset[i] = dataset[i].translate(trantab)
        pass
    return dataset
