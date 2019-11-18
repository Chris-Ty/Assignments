import os
import tarfile
import sys
from collections import defaultdict
import readFileTest_22

# data_root = '/Users/zhengtianyu/Documents/Cris-Mac/EntryTest/Lecture/Lesson9-8.30/' # 压缩包存储目录
# train_filename = 'notMNIST_large.tar.gz' # 该目录下的压缩包名称
# # train_filename = os.path.join(data_root, t_filename)

# 读取外部文件中的配置路径，等同于上边注释掉的代码
dirs = readFileTest_22.read_dir_conf('file_dir_conf')
data_root = dirs['data_root']
train_filename = dirs['train_filename']


def extract(data_root, filename):

    """
    将tar.gz打包的压缩文件解压缩
    :param data_root:文件目录
    :param filename:文件名
    :return:1个解压后的路径+文件夹的列表
    """

    target_file = os.path.join(data_root, filename)

    # remove suffix, .tar.gz
    pureName = os.path.splitext(os.path.splitext(target_file)[0])[0]


    # 判断上述无后缀文件是否已存在
    if os.path.isdir(pureName):
        print('{0}已存在，无需解压缩{1}\n----------'.format(pureName, filename))
    else:
        print('正在为您解压{0}...'.format(filename))
        tar = tarfile.open(filename)
        tar.extractall(data_root) # 参数path:str='.' 根目录 要解压到的位置
        tar.close()

    # 将要返回的多文件列表——组合（路径+文件名）
    data_folders = [os.path.join(pureName, d)for d in sorted(os.listdir(pureName))
                    if os.path.isdir(os.path.join(pureName, d))]

    return data_folders


if __name__ == '__main__':
    # Test
    d_f = extract(data_root, train_filename)

    for f in d_f:
        print(f)

