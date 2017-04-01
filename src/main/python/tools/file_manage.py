"""
操作管理文件的api
"""
import os, random, string, shutil
import configparser
from tools import logger
from context import resource_manager
from tools import config_parser
import time
log = logger.getLogger()


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

path=".";
src="./src";
#path=raw_input("src path:");
directorys=os.listdir(src);
i=0;

"""


# get sub dirs
def subdirs(path):
    dl = [];
    for i in os.walk(path, False):
        for d in i[1]:
            dl.append(os.path.join(path, d))
    return dl


# get sub file
def subfiles(path):
    fl = [];
    for i in os.walk(path, False):
        for f in i[2]:
            fl.append(os.path.join(path, f))
    return fl


def subfilesName(path):
    fl = [];
    for i in os.walk(path, False):
        for f in i[2]:
            fl.append(f)
    return fl

def fix_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def random_string(randomlength=8):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])


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
            p=i[0]
            dl.append(os.path.join(p, d))
    return dl


def subSimplefilesName(path):
    """
    得到对应路径下的，相关文件
    """
    # log.debug(path)
    fl = [];
    for i in os.walk(path, False):
        for f in i[2]:
            fl.append(f)
    # log.debug(fl)
    return fl


def sub_files_path_name(directory):
    fl = []
    subdir = os.listdir(directory)
    """
    for i in os.walk(path, False):
        for f in i[2]:
            fl.append(f)
    """
    for i in subdir:
        path = os.path.join(directory, i)
        if os.path.isdir(path):
            fl.extend(subfilesName(path))
        elif os.path.isfile(path):
            fl.append(path)
    return fl


# get sub file
def subfiles(path):
    fl = [];
    for i in os.walk(path, False):
        for f in i[2]:
            fl.append(os.path.join(path, f))
    return fl


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    randomlength=int(randomlength)
    #r = random.random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def random_string(randomlength=8):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])


def _time_name():
    #%H%M%S
    t=time.strftime("%H%M%S", time.localtime())
    return t



def rename_dir(url, reverse=False):
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

    """
    用户给定文件夹的路径，如果给定路径存在，更改指定文件夹下的文件夹的名字
    :param url: 用户给定的文件夹的路径
    :param reverse: 如果reverse=True就进行反向命名，reverse=False就对所给文件夹所包含的文件夹进行重命名；
    :return:
    """
    if _exist_(url) and reverse == False:
        if not os.path.exists(url):
            url = os.path.abspath(url)
        a =  1
        list_sto = random_name(url, 'D')
        con=config_parser.ConfigParser("D")
        """
            while (True):
            if str(a) in list_sto:
                a = a + 1
            else:
                break
        """
        conf_sto = configparser.ConfigParser()
        conf_sto.read('conf' + resource_manager.getSeparator() + 'directory.ini')
        for ob in list_sto:
            try:
                files = conf_sto.get(url, ob)
                old = os.path.join(url, files);
                filetype = os.path.splitext(files)[1];
                d = a
                if os.path.isdir(old):
                    New = os.path.join(url, str(a) + filetype);
                    a = str(a) + filetype
                    os.rename(old, New);
                    _store_(con,url, ob, a)
                    a = d
                    a = a + 1
            except:
                pass;
        con.save()
    elif reverse == True and _exist_(url):
        _reverse_(url, 'D')

def rename(config,url,old,new):
    New = url+new
    Old=url+old
    os.rename(Old, New)
    _store_(config,url, old, new)





def rename_files(url, reverse=False):
    log.info("starting rename files in "+str(url))
    """
        用户给定文件夹的路径，如果给定路径存在，更改指定文件夹下的文件的名字
        :param url: 用户给定的文件夹的路径
        :param reverse: 如果reverse=True就进行反向命名，reverse=False就对所给文件夹所包含的文件进行重命名；
        :return:
    """
    if _exist_(url) and reverse == False:
        if not os.path.exists(url):
            url = os.path.abspath(url)
        a = 1
        list_sto = random_name(url, 'F')
        con=config_parser.ConfigParser("F")
        """
        while (True):
            if str(a) in list_sto:
                a = a + 1
            else:
                break
        """
        # conf_sto = configparser.ConfigParser()
        # conf_sto.read('conf' + resource_manager.getSeparator() + 'document.ini')
        for ob in list_sto:
                files = con.getValue(url, ob)
                old = os.path.join(url, files);
                filetype = os.path.splitext(files)[1];
                d = a
                if os.path.isfile(old):
                    New = os.path.join(url, str(_time_name())+"_"+str(a) + filetype);
                    a = str(a) + filetype
                    os.rename(old, New);
                    _store_(con,url, ob, str(_time_name())+"_"+str(a)+filetype)
                    a = d
                    a = a + 1
        con.save()

    elif reverse == True and _exist_(url):
        _reverse_(url, 'F')


"""根据reverse进行反向目录生成"""


def _reverse_(doc_name, type):
    """
    根据reverse进行反向目录生成
    :param doc_name: 用户给定文件夹的路径
    :param type: 根据用户调用方法的不同对文件和文件夹分开进行重命名；type=‘F（file）’对文件操作，type=‘D（directory）’对文件夹操作
    :return:
    """
    try:
        conf = configparser.ConfigParser()
        if type == 'D':
            conf.read('conf' + resource_manager.getSeparator() + 'directory.ini')
        elif type == 'F':
            conf.read('conf' + resource_manager.getSeparator() + 'document.ini')
        options = conf.options(doc_name)
        if not os.path.exists(doc_name):
            doc_name = os.path.abspath(doc_name)
        for option in options:
            try:
                str_val = conf.get(doc_name, option)
                New = os.path.join(doc_name, option);
                old = os.path.join(doc_name, str_val);
                os.rename(old, New);
            except:
                print(option + "  don't exist")
    except:
        print("no document has been renamed")


def _exist_(url):
    """
    判断所给的路径是否存在,如果所给的是相对路径（在判断文件夹不存在后）转换为绝对路径
    :param url: 用户给定文件夹的路径
    :return:
    """
    s = url;
    if not os.path.exists(url):
        s = os.path.abspath(url)
    if os.path.exists(s) and os.path.isdir(s):
        return True
    else:
        print(url + " don't exist or isn't a dir")


def _store_(c,section, key, value):
    """
    将更改后的文件oldname和newname以section的方式存到directory.ini或factory.ini中
    （具体哪个文件夹则根据所给的文件类型type决定，用户调用相应的方法后type自动赋值）
    :param doc_name:用户传入的文件夹的路径
    :param files:文件夹下面的文件或文件夹（具体类型根据type决定）的名字
    :param a:文件重命名后新的编码（名字）
    :return:
    """
    c.addValue(section,key,value)




def random_name(url, type):
    """
    对文件或文件夹进行随机重命名（防止产生因同名而无法重命名的问题）（具体类型则根据所给的文件类型type决定，用户调用相应的方法后type自动赋值）
    :param url: 用户传入的文件夹的地址
    :return: 返回文件夹中所有文件或文件夹重命名之前的名字的列表
    """

    if not os.path.exists(url):
        url=resource_manager.Properties.getRootPath() + resource_manager.getSeparator() +url
    doc = os.listdir(url)
    if type == 'D':
        con=config_parser.ConfigParser('D')
    else:
        con=config_parser.ConfigParser('F')
    for files in doc:
            filetype = os.path.splitext(files)[1]
            if  os.path.exists(url):
                old=url+resource_manager.getSeparator()+files
            else:
                old=resource_manager.Properties.getRootPath()+resource_manager.getSeparator()+url+resource_manager.getSeparator()+files

            if os.path.isdir(old) and type=='D':
                random = random_string()

                New = url + resource_manager.getSeparator() + random+ filetype
                os.rename(old, New);
                _store_(con,url, files, random + filetype)
            elif os.path.isfile(old) and type=='F':
                random = random_string()

                if  os.path.exists(url):
                    New =  url + resource_manager.getSeparator() + random+ filetype
                else:
                    New = url + resource_manager.getSeparator() + random

                os.rename(old, New);
                _store_(con,url, files, random + filetype)
    con.save()
    list = doc
    return list;


def renamefiles(src=resource_manager.Properties.getDefaultOperationFold()):
    log.info("starting rename file job.")
    directorys = os.listdir(src)
    cf=config_parser.ConfigParser("F")
    c = 0
    for directory in directorys:
        if os.path.isdir(src + resource_manager.getSeparator() + directory):
            files = subfilesName(src + resource_manager.getSeparator() + directory)
            c += len(files)
            log.info(str(
                "####" + src + resource_manager.getSeparator() + directory + " directory is doing #### " + str(len(files))))
            path = src + resource_manager.getSeparator() + directory
            for f in files:
                # log.info(os.path.join(f)+"....")
                if os.path.isfile(os.path.join(path, f)) == True:
                    c=c+1
                    # name = '{0}_{1:0{2}d}'.format(directory, c, 6)
                    name = '_{0}_{1}{2:0{3}d}'.format(directory, _time_name(),c,4)
                    name= random_string()+name
                    rename(cf,src+resource_manager.getSeparator()+directory+resource_manager.getSeparator(),f,name)

        else:
            c=c+1
            s=src.split(resource_manager.getSeparator())
            s=s[(len(s)-1)]
            # name = '_{0}_{1:0{2}d}'.format(s, _time_name(), 6)
            name = '_{0}_{1}{2:0{3}d}'.format(s, _time_name(),c,4)
            name= random_string()+name
            rename(cf,src+resource_manager.getSeparator(),directory,name)


    log.info("finish rename " + str(c) + " job.")
    cf.save()





if __name__=="__main__":
    path=resource_manager.Properties.getDefaultDataFold()
    rename_dir(path+"finalclusters/Finalclusters/")

    #rename_files(url= path + "cache")