import data_manager
from model import BoW

HAMILTON_TRAIN_LIST = [1, 6, 7, 8, 9, 11, 12, 13, 15, 16, 17, 21, 22, 23, 24, 25, 26, 27, 28, 29]
HAMILTON_TEST_LIST = [9, 11, 12]
MADISON_TRAIN_LIST = [10, 14, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 58]
MADISON_TEST_LIST = [47, 48, 58]
TEST_LIST = [49, 50, 51, 52, 53, 54, 55, 56, 57, 62, 63]


dataset_path = '../dataset/'
n = 1
# Which documents are the test data?
test_list = HAMILTON_TEST_LIST

data_manager.update_punctuations(n)


def train():
    # Hamilton data
    training_data = data_manager.read(HAMILTON_TRAIN_LIST, dataset_path)
    train_dataset = training_data[0]

    # Madison data
    training_data_madison = data_manager.read(MADISON_TRAIN_LIST, dataset_path)
    train_dataset_madison = training_data_madison[0]

    model1 = BoW()
    model2 = BoW()

    # Hamilton train
    train_dataset = data_manager.pre_process(train_dataset, n_gram=n)
    model1.train(train_dataset, n_gram=n)

    model1.save(path='../models/', name='model_hamilton_' + str(n))

    # Madison train
    train_dataset_madison = data_manager.pre_process(train_dataset_madison, n_gram=n)
    model2.train(train_dataset_madison, n_gram=n)

    model2.save(path='../models/', name='model_madison_' + str(n))


def test(model_hamilton, model_madison):
    # Test Data
    test_data = data_manager.read(test_list, dataset_path)
    test_labels = test_data[1]
    test_dataset = test_data[0]

    test_dataset = data_manager.pre_process(test_dataset, n_gram=n)

    ham_predictions = model_hamilton.test(test_dataset)

    mad_predictions = model_madison.test(test_dataset)

    predictions = []
    for i in range(len(ham_predictions)):
        if ham_predictions[i] < mad_predictions[i]:
            predictions.append(data_manager.Label.MADISON)
        else:
            predictions.append(data_manager.Label.HAMILTON)

    print(predictions)


train()
