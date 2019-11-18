import pickle
import numpy as np
import explore_3

image_size = explore_3.image_size


def make_arrays(nb_rows, img_size):
    """
    :param nb_rows: 数据行数
    :param img_size: 像素点数
    :return: 生成的数据集与标签
    """
    if nb_rows:
        dataset = np.ndarray((nb_rows, img_size, img_size), dtype=np.float32)
        labels = np.ndarray(nb_rows, dtype=np.int32)
    else:
        dataset, labels = None, None
    return dataset, labels

def merge_datasets(pickle_files, train_size, valid_size=0):
    """
    :param pickle_files: 之前将图片文件打包成的二进制文件列表
    :param train_size: 顾名思义
    :param valid_size: 默认0
    :return:
    """

    global image_size

    num_classes = len(pickle_files) # 类别数=len(打包的A-J)
    train_dataset, train_labels = make_arrays(train_size, image_size)
    valid_dataset, valid_labels = make_arrays(valid_size, image_size)  # (行数, 像素点数：28)
    vsize_per_class = valid_size // num_classes  # 理解到valid_size大概是验证集数量，那么vsize_per_class就是分配到每个类别的验证集数量
    tsize_per_class = train_size // num_classes  #

    start_v, start_t = 0, 0  # 验证集起始位置
    end_v, end_t = vsize_per_class, tsize_per_class  #
    end_l = vsize_per_class + tsize_per_class  # 做索引用

    for label, pickle_file in enumerate(pickle_files):
        try:
            with open(pickle_file, 'rb') as f:
                letter_set = pickle.load(f)
                # 让我们对字母进行洗牌以获得随机的验证和训练集
                np.random.shuffle(letter_set)

                if valid_dataset is not None: # 验证集可能为0(coders设置)
                    valid_letter = letter_set[:vsize_per_class, :, :]  # 所有的ndarray切到验证集数量
                    valid_dataset[start_v:end_v, :, :] = valid_letter # 验证数据集中(不含标签)，类别索引估计会在下边的代码中出现
                    valid_labels[start_v:end_v] = label # 0-9 验证集数据的标签部分
                    start_v += vsize_per_class  # 索引控制，索引切到下一个类别(A-B-C....J)中
                    end_v += vsize_per_class # 同上

                # 接下来处理训练数据，基本切分思路同上，
                train_letter = letter_set[vsize_per_class:end_l, :, :]  # ?感觉和验证集里的B-J的数据重复，再看
                train_dataset[start_t: end_t, :, :] = train_letter
                train_labels[start_t: end_t] = label
                start_t += vsize_per_class
                end_t += vsize_per_class

        except Exception as e:
            print('不能从{0}处理数据:{1}'.format(pickle_file, e))
            raise

    return valid_dataset, valid_labels, train_dataset, train_labels
