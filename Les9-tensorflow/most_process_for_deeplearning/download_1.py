import os
from urllib.request import urlretrieve

# def cbk(a,b,c):
#     '''
#
#     :param a: 已经下载的数据块
#     :param b: 数据块的大小
#     :param c: 远程文件的大小
#     :return:
#     '''
#
#     per=100.0*a*b/c
#     if per>100:
#         per=100
#     print('%.2f%%' % per)
#
# url='http://www.python.org/ftp/python/2.7.5/Python-2.7.5.tar.bz2'
# dir=os.path.abspath('.')
# work_path=os.path.join(dir,'Python-2.7.5.tar.bz2')
# urlretrieve(url,work_path,cbk)

def download(url, savepath='./'):
    """
    download file from internet
    :param url: path to download from
    :param savepath: path to save files
    :return: None
    """
    def reporthook(a,b,c):
        """
        显示下载进度
        :param a: 已经下载的数据块
        :param b: 数据块的大小
        :param c: 远程文件大小
        :return: None
        """
        print("\rdowloing: {0}%".format(a * b / c * 100), end=" ")

    filename = os.path.basename(url)
    # 判断文件是否存在，如果不存在则下载
    if not os.path.isfile(os.path.join(savepath, filename)):
        print('Downloading data from %s' % url)
        urlretrieve(url, os.path.join(savepath, filename), reporthook=reporthook)
        print('\nDownload finished!')
    else:
        print('File already exits!')

    # 获取文件大小
    filesize = os.path.getsize(os.path.join(savepath, filename))
    # print(filesize)
    if filesize == 0:
        os.remove(os.path.join(savepath, filename))
    # 文件大小默认以Bytes计， 转换为Mb
    print('File size = %.2f Mb' % (filesize/1024/1024))

if __name__ == '__main__':
    url = 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz'
    download(url, savepath='./')


# https://inews.gtimg.com/newsapp_bt/0/10539171803/1000
# 数据集下载地址是：url = 'https://commondatastorage.googleapis.com/books1000/'
# 该模块要重写，要优化代码以匹配文件大小判断是否下载完全。