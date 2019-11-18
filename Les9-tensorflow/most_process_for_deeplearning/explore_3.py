"""
=====
探索数据
用到概念：归一化
用到了imageio读取图片和cPickle写入文件
"""
import os
import numpy as np
from extract_2 import extract
from readFileTest_22 import read_dir_conf
import imageio
from six.moves import cPickle as pickle
from tqdm import tqdm

image_size = 28  # Pixel像素 width and height.
pixel_depth = 255.0  # Number of levels per pixel. 每个像素点的大小

# 写函数首先要明确目标是什么
def maybe_pickle(data_folders, min_num_images_per_class, force=False):
    """
    :param data_folders:
    :param min_num_images_per_class:
    :param force:
    :return:.pickle文件们的列表(A-J)
    """
    dataset_names = []
    # 遍历根目录(data_folder)下，依次访问A - J的文件夹
    for folder in data_folders:
        set_filename = folder + '.pickle'
        dataset_names.append(set_filename)
        if os.path.exists(set_filename):  # optimal parameter:force=False
            print(('{}s already present - Skipping pickling.已存在，略过打包。'.format(set_filename)))

        else:
            print('Pickling {}'.format(set_filename))
            dataset = load_letter(folder, min_num_images_per_class)
            try:
                with open(set_filename, 'wb') as f:
                    pickle.dump(dataset, f, pickle.HIGHEST_PROTOCOL)
            except Exception as e:
                print('不能保存数据到', set_filename, ':', e)

    return dataset_names # 值返回pickle的文件名列表，而非将数据直接返回



def load_letter(folder, min_num_images):
    """
    为每个单独的字母标签加载数据
    维度：图片书*像素点行数*像素点列数
    :param folder: 一个字母命名的单个文件夹，内含若干着28*28像素的若干图片
    :param min_num_images: 要求内含最终用于训练的最小图片个数
    :return: a ndarray whose shape=(len(image_files), image_size, image_size)
    """

    global image_size, pixel_depth

    image_files = os.listdir(folder)  # 列出每个A-J文件夹内各自的全部图片
    # 生成图片数目*28*28维度的dataset
    dataset = np.ndarray(shape=(len(image_files), image_size, image_size), dtype=np.float32)
    num_images = 0  # 做图片索引（A文件夹内）
    # 再依次遍历每个图片，获取其路径
    for image in image_files:
        image_file = os.path.join(folder, image)  # 单个图片文件
        # 加载图片数据
        try:
            # 暂时理解为类似归一化
            image_data = (imageio.imread(image_file).astype(float) -
                          pixel_depth / 2) / pixel_depth
            if image_data.shape != (image_size, image_size):
                raise Exception('非预期的28*28的图片像素维度，而是：{0}'.format(image_data.shape))
            dataset[num_images, :, :] = image_data
            num_images += 1
        except (IOError, ValueError) as e:
            print('Could not read:{0}:{1}- it\'s ok, skipping.'.format(image_file, e))

    dataset = dataset[0:num_images, :, :]  # 废话代码？
    if num_images < min_num_images:
        raise Exception('比预期的图像少：{}<{}'.format(num_images, min_num_images))

    print('（该文件夹下）全部dataset tensor张量：{0}'.format(dataset.shape))
    print('平均值Mean：{0}'.format(np.mean(dataset)))  # 全部值的均值，类似灰度，疑问的地方是图片号数也加入了均值计算
    print('标准差Standard deviation：{0}'.format(np.std(dataset)))

    return dataset


if __name__ == '__main__':

    # 获得文件路径
    dirs = read_dir_conf('file_dir_conf')
    data_root = dirs['data_root']
    train_filename = dirs['train_filename']
    test_filename = dirs['test_filename']
    print('文件路径分别为:\n{}\n与\n{}'.format(os.path.join(data_root, train_filename), os.path.join(data_root, test_filename)))

    # 提取压缩包内的内容
    train_folders = extract(data_root, train_filename) # A-J的文件夹路径+文件名组成的路径集合
    test_folders = extract(data_root, test_filename)

    train_datasets = maybe_pickle(train_folders, 45000)
    test_datasets = maybe_pickle(test_folders, 1800)

    print(len(train_datasets))
    print(len(test_datasets))
