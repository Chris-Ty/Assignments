import numpy as np

def randomize(dataset, labels):
    """
    Next, we'll randomize the data. It's important to have the labels well shuffled for the training and test
    distributions to match.

    :param dataset:数据集
    :param labels:标签（此函数通过标签乱序后作为索引引导数据）
    :return: 顺序后的数据集和标签
    """

    permutation = np.random.permutation(labels.shape[0])  # labels.shape[0]=行数如10000，但permutation返回类型为ndarray，很好奇它是如何作为切片索引的。
    shuffled_dataset = dataset[permutation, :, :]  # 略微?
    shuffled_labels = labels[permutation]

    return shuffled_dataset, shuffled_labels
