import os
import configparser
from context import resource_manager
from tools import file_manage


def rename_dir(url,reverse=True):
    """
    用户给定文件夹的路径，如果给定路径存在，更改指定文件夹下的文件夹的名字
    :param url: 用户给定的文件夹的路径
    :param reverse: 如果reverse=True就进行反向命名，reverse=False就对所给文件夹所包含的文件夹进行重命名；
    :return:
    """
    if _exist_(url)and reverse==False:
        if not os.path.exists(url):
            url = os.path.abspath(url)
        a = 1
        list_sto=_random_name(url,'D')
        while(True):
            if str(a) in list_sto:
                a=a+1
            else:
                break
        conf_sto = configparser.ConfigParser()
        conf_sto.read('conf'+resource_manager.getSeparator()+'directory.ini')
        for ob in list_sto:
            try:
                files=conf_sto.get(url,ob)
                old=os.path.join(url,files);
                filetype=os.path.splitext(files)[1];
                d=a
                if os.path.isdir(old):
                    New=os.path.join(url,str(a)+filetype);
                    a=str(a)+filetype
                    os.rename(old, New);
                    _store_(url,ob,a,'D')
                    a=d
                    a=a+1
            except:
                pass;
    elif reverse==True and _exist_(url):
        _reverse_(url,'D')

def rename_file(url,reverse=True):
    """
        用户给定文件夹的路径，如果给定路径存在，更改指定文件夹下的文件的名字
        :param url: 用户给定的文件夹的路径
        :param reverse: 如果reverse=True就进行反向命名，reverse=False就对所给文件夹所包含的文件进行重命名；
        :return:
        """
    if _exist_(url)and reverse==False:
        if not os.path.exists(url):
            url = os.path.abspath(url)
        a = 1
        list_sto=_random_name(url,'F')
        while(True):
            if str(a) in list_sto:
                a=a+1
            else:
                break
        conf_sto = configparser.ConfigParser()
        conf_sto.read('conf'+resource_manager.getSeparator()+'factory.ini')
        for ob in list_sto:
            try:
                files=conf_sto.get(url,ob)
                old=os.path.join(url,files);
                filetype=os.path.splitext(files)[1];
                d=a
                if os.path.isfile(old):
                    New=os.path.join(url,str(a)+filetype);
                    a=str(a)+filetype
                    os.rename(old, New);
                    _store_(url,ob, a,'F')
                    a=d
                    a=a+1
            except:
                pass;
    elif reverse==True and _exist_(url):
        _reverse_(url,'F')


"""根据reverse进行反向目录生成"""
def _reverse_(doc_name,type):
    """
    根据reverse进行反向目录生成
    :param doc_name: 用户给定文件夹的路径
    :param type: 根据用户调用方法的不同对文件和文件夹分开进行重命名；type=‘F（file）’对文件操作，type=‘D（directory）’对文件夹操作
    :return:
    """
    try:
        conf = configparser.ConfigParser()
        if type=='D':
            conf.read('conf'+resource_manager.getSeparator()+'directory.ini')
        elif type=='F':
            conf.read('conf'+resource_manager.getSeparator()+'factory.ini')
        options = conf.options(doc_name)
        if not os.path.exists(doc_name):
            doc_name = os.path.abspath(doc_name)
        for option in options:
            try:
                str_val = conf.get(doc_name,option )
                New=os.path.join(doc_name,option);
                old=os.path.join(doc_name,str_val);
                os.rename(old,New);
            except:
                print(option+"  don't exist")
    except:
        print("no document has been renamed")


def _exist_(url):
    """
    判断所给的路径是否存在,如果所给的是相对路径（在判断文件夹不存在后）转换为绝对路径
    :param url: 用户给定文件夹的路径
    :return:
    """
    s=url;
    if not os.path.exists(url):
        s = os.path.abspath(url)
    if os.path.exists(s) and os.path.isdir(s):
        return True
    else:
        print(url + " don't exist or isn't a dir")


def _store_(doc_name,files,a,type):
    """
    将更改后的文件oldname和newname以section的方式存到directory.ini或factory.ini中
    （具体哪个文件夹则根据所给的文件类型type决定，用户调用相应的方法后type自动赋值）
    :param doc_name:用户传入的文件夹的路径
    :param files:文件夹下面的文件或文件夹（具体类型根据type决定）的名字
    :param a:文件重命名后新的编码（名字）
    :return:
    """
    try:
        config_write = configparser.ConfigParser()
        if type=='D':
            config_write.read('conf'+resource_manager.getSeparator()+'directory.ini')
            ftest = open('conf'+resource_manager.getSeparator()+'directory.ini','w+')
        elif type=='F':
            config_write.read('conf'+resource_manager.getSeparator()+'factory.ini')
            ftest = open('conf'+resource_manager.getSeparator()+'factory.ini','w+')
        check=config_write.sections()
        n=False
        if doc_name in check:
            n=True
            config_write.set(doc_name,files,str(a))
        if n==False:
            config_write.add_section(doc_name)
            config_write.set(doc_name,files,str(a))
        config_write.write(ftest)
        ftest.close()
    except:
        pass;


def _random_name(url,type):
    """
    对文件或文件夹进行随机重命名（防止产生因同名而无法重命名的问题）（具体类型则根据所给的文件类型type决定，用户调用相应的方法后type自动赋值）
    :param url: 用户传入的文件夹的地址
    :return: 返回文件夹中所有文件或文件夹重命名之前的名字的列表
    """
    doc=os.listdir(url)
    for files in doc:
        try:
            filetype=os.path.splitext(files)[1]
            old=resource_manager.Properties.getRootPath()+resource_manager.getSeparator()+url+resource_manager.getSeparator()+files
            if os.path.isdir(old)and type=='D':
                random=file_manage.random_string()
                New=resource_manager.Properties.getRootPath()+resource_manager.getSeparator()+url+resource_manager.getSeparator()+random
                os.rename(old, New);
                _store_(url,files,random+filetype,'D')
            elif os.path.isfile(old)and type=='F':
                random=file_manage.random_string()
                New=resource_manager.Properties.getRootPath()+resource_manager.getSeparator()+url+resource_manager.getSeparator()+random
                os.rename(old, New);
                _store_(url,files,random+filetype,'F')
        except:
            pass
    list=doc
    return list;


if __name__ == "__main__":
    rename_file(url='qxy/otest',reverse=True)
    rename_dir(url='qxy/otest',reverse=True)








