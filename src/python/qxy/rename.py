import os
import logging
import re
import configparser

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
"""根据reverse进行反向目录生成"""
def _reverse_(doc_name):

    conf = configparser.ConfigParser()
    conf.read("directory")
    options = conf.options(doc_name)
    if not os.path.exists(doc_name):
        url = os.path.abspath(doc_name)#如果路径不存在，得到绝对路径
    for option in options:
        str_val = conf.get(doc_name,option )
        New=os.path.join(doc_name,option);
        old=os.path.join(doc_name,str_val);
        print(old+"\n"+New)
        os.rename(New,old);



"""如果给定路径存在，更改指定文件夹下的文件名"""

def rename_dir(url,static=True,reverse=True):

    if _exist_(url)and reverse:
        if not os.path.exists(url):
            url = os.path.abspath(url)#如果路径不存在，得到绝对路径
        a = 0
        doc=os.listdir(url)
        print(os.path.basename(url))
        for files in doc:
            old=os.path.join(url,files);
            filetype=os.path.splitext(files)[1];
            #filetype=os.path.splitext(files);#文件扩展名
            New=os.path.join(url,str(a)+filetype);#新的文件路径
            print(old+"\n"+New)
            os.rename(old, New);
            _store_(url,files, a)
            a=a+1
    else:
        _reverse_(url)


"""判断所给的路径是否存在"""
def _exist_(url):
    """ s=os.path.abspath('../test')
    print(s)
    print(os.path.exists(s),os.path.isdir(s))"""
    s=url;
    if not os.path.exists(url):
        s = os.path.abspath(url)
        print(s)
    print(os.path.exists(s),os.path.isdir(s))
    if os.path.exists(s) and os.path.isdir(s):
        return True
    else:
        print(url + " don't exist or isn't a dir")

"""将更改后的文件oldname和newname以section的方式存到directory中"""
def _store_(doc_name,files, a):
    """

    :param doc_name:
    :param files:
    :param a:
    :return:
    """

    config_write = configparser.ConfigParser()
    config_write.read("directory")
    check=config_write.sections()
    print("check:"+ str(check))
    n=False
    if doc_name in check:
        n=True
        config_write.set(doc_name,files,str(a))

    if n==False:
        config_write.add_section(doc_name)
        config_write.set(doc_name,files,str(a))
    ftest = open('directory','w+')
    config_write.write(ftest)
    ftest.close()
    print(n)


if __name__ == "__main__":
    rename_dir(url="otest/abccc",static=True,reverse=False)








