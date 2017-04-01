import os
import logging
import numpy as np




def rename_dir(url,reverse=True):
    """"
    根据static的值进行文件夹自动重命名，命名规则
    YYYYMMDDhhmmsss+3[001]
    directory.ini
    网->0
    于->1
    :param url:,文件夹地址，
    :param static:给出的需要进是关于地址是否是相对地址
    :param reverse:确定是行反向目录生成，还是正向目录生成
    :return:
    Tip：需要判断url是否存在，是否为文件夹,对于conf目录需要注意是否已经存在，没有存在需要进行创建。另外对于directory.ini文件也需要判断是否存在。
    建议对这里的工作进行定义多个子函数。定义的子函数请以_开头。
    在进行一些具体的操作，需要输出相关日志操作
    """""
    if _exist_(url):
        print(os.listdir(url))
        url = os.path.abspath(url)
        print(url,"\n")
        a = 0
        doc=os.listdir(url)
        print(os.path.basename(url))
        for files in doc:
            doc_name=os.path.splitext(files);#文件名
        #filetype=os.path.splitext(files);#文件扩展名
        #Newdir=os.path.join(path,str(count)+filetype);#新的文件路径
            print(files)
            os.renames(files, "b")
            _store_(doc_name, a)
            ++a


def _exist_(url):
    """ s=os.path.abspath('../ssdfdssdf')
    print(s)
    print(os.path.exists(s),os.path.isdir(s))"""
    if os.path.exists(url):
        s=url
    else:
        s = os.path.abspath(url)
    print(s)
    print(os.path.exists(s),os.path.isdir(s))
    if os.path.exists(s) and os.path.isdir(s):
            return True
    else:
        print(url + " don't exist or isn't a dir")


def _store_(doc_name, a):
    store = open("directory.ini", "w+")
    list = [doc_name, '=', a]
    store.write(list)
    store.append("\n")
    store.close()


if __name__ == "__main__":
    rename_dir(url='D:\Work\Workspace\liber\src\\python\\ssdfdssdf\\abc',static=True,reverse=True)








