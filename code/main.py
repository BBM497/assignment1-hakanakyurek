import data_manager
from model import BoW

HAMILTON_TRAIN_LIST = [1, 6, 7, 8, 9, 11, 12, 13, 15, 16, 17, 21, 22, 23, 24, 25, 26, 27, 28, 29]
HAMILTON_TEST_LIST = [9, 11, 12]
MADISON_TRAIN_LIST = [10, 14, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 58]
MADISON_TEST_LIST = [47, 48, 58]
TEST_LIST = [2, 3, 4, 5, 10, 18, 19, 20, 30, 31, 32, 33, 34, 35, 36, 49]

dataset_path = '../dataset/'
n = 1

data_manager.update_punctuations(n)

# Hamilton data
training_data = data_manager.read(HAMILTON_TRAIN_LIST, dataset_path)
train_labels = training_data[1]
train_dataset = training_data[0]

# Madison data
training_data_madison = data_manager.read(MADISON_TRAIN_LIST, dataset_path)
train_labels_madison = training_data_madison[1]
train_dataset_madison = training_data_madison[0]

test_data = data_manager.read(HAMILTON_TEST_LIST, dataset_path)
test_labels = test_data[1]
test_dataset = test_data[0]

test_dataset = data_manager.pre_process(test_dataset, n_gram=n)

model_hamilton = BoW()
model_madison = BoW()

# Hamilton train
train_dataset = data_manager.pre_process(train_dataset, n_gram=n)
model_hamilton.train(train_dataset, n_gram=n)
# print(model_hamilton.test(test_dataset))
model_hamilton.generate()
'''
# Madison train
train_dataset_madison = data_manager.pre_process(train_dataset_madison, n_gram=n)
model_madison.train(train_dataset_madison, n_gram=n)
print(model_madison.test(test_dataset))
'''
