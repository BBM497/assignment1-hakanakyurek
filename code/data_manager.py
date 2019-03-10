import os
import enum


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
