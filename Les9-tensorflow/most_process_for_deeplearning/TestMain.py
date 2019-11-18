import extract_2
import readFileTest_22
import explore_3
import mergeData_4
import shuffle_5

import os
import pickle


dirs = readFileTest_22.read_dir_conf('file_dir_conf')
print(dirs)

data_root = dirs['data_root']
train_filename = dirs['train_filename']
test_filename = dirs['test_filename']

train_folders = extract_2.extract(data_root, train_filename)
test_folders = extract_2.extract(data_root, test_filename)


train_data_sets = explore_3.maybe_pickle(train_folders, 45000)
test_data_sets = explore_3.maybe_pickle(test_folders, 1800)

# print(test_data_sets[0:1])  # ['/Users/zhengtianyu/Documents/Cris-Mac/EntryTest/Lecture/Lesson9-8.30/notMNIST_Small/A.pickle']

train_size = 200000
valid_size = 10000
test_size = 10000

valid_dataset, valid_labels, train_dataset, train_labels = mergeData_4.merge_datasets(train_data_sets,
                                                                                      train_size,
                                                                                      valid_size)
_, _, test_dataset, test_labels = mergeData_4.merge_datasets(test_data_sets,
                                                             test_size)

print('Training：', train_dataset.shape, train_labels.shape)
print('Validation：', valid_dataset.shape, valid_labels.shape)
print('Testing：', test_dataset.shape, test_labels.shape)

# 5：shuffle
train_dataset, train_labels = shuffle_5.randomize(train_dataset, train_labels)
test_dataset, test_labels = shuffle_5.randomize(test_dataset, test_labels)
valid_dataset, valid_labels = shuffle_5.randomize(valid_dataset, valid_labels)

print(test_dataset.shape)

pickle_file = os.path.join(data_root, 'notMNIST.pickle')
try:
    with open(pickle_file, 'wb') as f:
        save = {
            'train_dataset': train_dataset,
            'train_labels': train_labels,
            'valid_dataset': valid_dataset,
            'valid_labels': valid_labels,
            'test_dataset': test_dataset,
            'test_labels': test_labels
        }
        pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
except Exception as e:
    print('不能存储数据至：{0}：{1}'.format(pickle_file, e))
    raise

statinfo = os.stat(pickle_file)
print('Compressed pickle size: %.2f' % (statinfo.st_size/1024/1024/1024), ' GB')
