"""
操作管理文件的api
"""
from PIL import Image
from numpy import genfromtxt
import gzip, cPickle
from glob import glob
import numpy as np
import pandas as pd

def rename_dir(url,static=True,reverse=True):
    """"
    根据static的值进行文件夹自动重命名，命名规则
    directory.ini
    网->0
    于->1
    :param url:,文件夹地址，
    :param static:给出的是关于地址是否是相对地址
    :param reverse:确定是需要进行方向目录生成，还是正向目录生成
    :return:
    Tip：需要判断url是否存在，是否为文件夹,对于conf目录需要注意是否已经存在，没有存在需要进行创建。另外对于directory.ini文件也需要判断是否存在。建议对这里的工作进行定义多个子函数。定义的子函数请以_开头。
    在进行一些具体的操作，需要输出相关日志操作
    """""





class pcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    Blue = '\34[95m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def dir_to_dataset(glob_files):
    # print("Gonna process:\n\t %s" % glob_files)
    dataset = []
    clazz = []
    for file_count, file_name in enumerate(sorted(glob(glob_files), key=len)):
        image = Image.open(file_name)
        # print file_name
        img = Image.open(file_name).convert('LA')  # tograyscale
        pixels = [f[0] for f in list(img.getdata())]
        dataset.append(pixels)
        classLabel = file_name.split("_")[1];
        # print file_name, "<--->", classLabel
        clazz.append(classLabel)
        if file_count % 1000 == 0:
            print("\t %s files processed" % file_count)
    # outfile = glob_files+"out"
    # np.save(outfile, dataset)
    return np.array(dataset), np.array(clazz)