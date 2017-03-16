"""
操作管理文件的api
"""
import os,random,string,shutil
from PIL import Image
from numpy import genfromtxt
from glob import glob
import numpy as np
import pandas as pd
import logging

logging.config.fileConfig("conf/logging.conf")
logger = logging.getLogger("root")
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
    BLUE = '\34[95m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


"""
    walk through a directory and get all the file in this directory.
"""


def subfilesName(directory):
    fl = []
    subdir=os.listdir(directory)
    """
    for i in os.walk(path, False):
        for f in i[2]:
            fl.append(f)
    """
    for i in subdir:
        path=os.path.join(directory,i)
        print(path)
        if os.path.isdir(path):
            fl.extend(subfilesName(path))
        elif os.path.isfile(path):
            fl.append(path)
            print("add"+path)
    return fl

"""

path=".";
src="./src";
#path=raw_input("src path:");
directorys=os.listdir(src);
i=0;

"""



def rename(path="./default_path"):

    directorys=os.listdir(path);
    for directory in directorys:
        logger.info("####"+directory+" is doing ####")
        path=path+"/"+directory;
        files=subfilesName(path)
        i=0;
        for f in files:
            logger.info(os.path.join(f),"....")
            if os.path.isfile(os.path.join(path,f))==True:
                i=i+1;
                name='{0}_{1:0{2}d}'.format(directory,i,4);
                logger.info(os.path.join(path,f)+" "+ os.path.join(path,name))
                os.rename(os.path.join(path,f),os.path.join(path,name));
                logger.info(f+" --> "+name)

# get sub dirs
def subdirs(path):
    """
    得到对应路径下的所有路径
    :param path:
    :return:
    """
    dl = [];
    for i in os.walk(path, False):
        for d in i[1]:
            dl.append(os.path.join(path, d))
    return dl

def subfilesName(path):
    """
    得到对应路径下的，相关文件
    """
    fl = [];
    for i in os.walk(path, False):
        for f in i[2]:
            fl.append(f)
    return fl

#get sub file
def subfiles(path):
    fl = [];
    for i in os.walk(path, False):
        for f in i[2]:
            fl.append(os.path.join(path, f))
    return fl

"""
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

"""

def random_string(randomlength=8):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])