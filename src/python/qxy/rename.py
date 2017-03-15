import os
import logging
import sys
import configparser




def rename_dir(url,static=True,reverse=True):
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
    """更改指定文件夹下的文件名"""
    if _exist_(url):
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
            _store_(old, a)
            a=a+1



"""""def rename():
    path="../abc"#"这里替换为你的文件夹的路径";
    filelist=os.listdir(path)#该文件夹下所有的文件（包括文件夹）
    for files in filelist:#遍历所有文件
        Olddir=os.path.join(path,files);#原来的文件路径
        filename=os.path.splitext(files)[0];#文件名
        filetype=os.path.splitext(files)[1];#文件扩展名
        Newdir=os.path.join(path,"1"+filetype);#新的文件路径
        os.renames(Olddir,Newdir);#重命名"""


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


def _store_(doc_name, a):

    ftest = open('directory.ini','+a')
    config_write = configparser.RawConfigParser()
    config_write.add_section(str(a))
    config_write.set(str(a),doc_name,str(a))
    config_write.write(ftest)
    ftest.close()


if __name__ == "__main__":
    rename_dir(url="otest",static=True,reverse=True)








