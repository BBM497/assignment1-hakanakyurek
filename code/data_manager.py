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
    UNKNOWN = 2


def read(data_list, path='./'):
    dataset = []
    labels = []

    for file in os.listdir(path):

        if int(file.split('.')[0]) in data_list:

            file = open(path + file, 'r')
            lines = file.readlines()

            if lines[0] == 'HAMILTON \n':
                label = Label.HAMILTON
            elif lines[0] == 'MADISON \n':
                label = Label.MADISON
            else:
                label = Label.UNKNOWN

            labels.append(label)
            dataset.append(lines[1])

            file.close()

    return dataset, labels


def pre_process(dataset, n_gram=1, remove_stopwords=False):
    """
    Applies preprocessing to the dataset: stopword removal, stemming, and lowercase.
    :param dataset: 2D array of string
    :param n_gram: N-gram value
    :param remove_stopwords: remove stopwords flag
    :return: preprocessed dataset
    """

    x = (n_gram - 1)

    for i in range(len(dataset)):
        dataset[i] = dataset[i].lower()

    dataset = filter_shortform(dataset)

    if remove_stopwords:
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
        for key in punctuations.keys(): punctuations[key] = x * end_token + punctuations[key] + x * start_token
    else:
        for key in punctuations.keys(): punctuations[key] = ' ' + punctuations[key]

    trantab = str.maketrans(punctuations)
    for i in range(len(dataset)):

        dataset[i] = dataset[i].translate(trantab)
        pass
    return dataset


def filter_shortform(dataset):

    import short_form
    a = short_form.short_all
    for i in range(len(dataset)):
        for key in short_form.short_all:
            dataset[i] = dataset[i].replace(key, short_form.short_all[key])

    return dataset
