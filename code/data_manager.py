import os


def read(path=''):
    train_dataset = []
    test_dataset = []

    train_path = path + 'Train/'
    for file in os.listdir(train_path):

        file = open(train_path + file, 'r')

        train_dataset.append(file.readlines())

        file.close()

    test_path = path + 'Test/'
    for file in os.listdir(test_path):

        file = open(test_path + file, 'r')

        test_dataset.append(file.readlines())

        file.close()

    return train_dataset, test_dataset

