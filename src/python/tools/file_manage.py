"""
操作管理文件的api
"""
import os,random,string,shutil
import  configparser
from tools import logger
from context import resource_manager

log=logger.getLogger()

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

path=".";
src="./src";
#path=raw_input("src path:");
directorys=os.listdir(src);
i=0;

"""


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

def subSimplefilesName(path):
    """
    得到对应路径下的，相关文件
    """
    #log.debug(path)
    fl = [];
    for i in os.walk(path, False):
        for f in i[2]:
            fl.append(f)
    #log.debug(fl)
    return fl

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
        if os.path.isdir(path):
            fl.extend(subfilesName(path))
        elif os.path.isfile(path):
            fl.append(path)
    return fl

#get sub file
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
    r = random.random()
    for i in range(randomlength):
        str+=chars[r.randint(0 ,length)]
    return str


def random_string(randomlength=8):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])



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
    conf=resource_manager.Properties.getDirectoryConfigPath()
    conf.read(conf)
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

def rename_dir(path=resource_manager.Properties.getDefaultOperationFold(),static=True,reverse=True):
    url=path
    if reverse is True:
        log.info("staring reverse director, from config setting.")
    else:
        log.info("starting rename director, save config setting.")

    if _exist_(url) and reverse:
        if not os.path.exists(url):
            url = os.path.abspath(url)#如果路径不存在，得到绝对路径
        a = 0
        doc=os.listdir(url)
        #print(os.path.basename(url))
        for files in doc:
            old=os.path.join(url,files);
            filetype=os.path.splitext(files)[1];
            #filetype=os.path.splitext(files);#文件扩展名
            New=os.path.join(url,str(a)+filetype);#新的文件路径
            #print(old+"\n"+New)
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
        log.info(str(s)+" is not exist.")
    #print(os.path.exists(s),os.path.isdir(s))
    if os.path.exists(s) and os.path.isdir(s):
        return True
    else:
        log.error(url + " don't exist or isn't a dir")

"""将更改后的文件oldname和newname以section的方式存到directory中"""
def _store_(doc_name,files, a):
    """

    :param doc_name:
    :param files:
    :param a:
    :return:
    """

    config_write = configparser.ConfigParser()
    conf=resource_manager.Properties.getDirectoryConfigPath()
    config_write.read(conf)
    check=config_write.sections()
    # print("check:"+ str(check))
    n=False
    if doc_name in check:
        n=True
        config_write.set(doc_name,files,str(a))

    if n==False:
        config_write.add_section(doc_name)
        config_write.set(doc_name,files,str(a))
    ftest = open(conf,'w+')
    config_write.write(ftest)
    ftest.close()


def rename_files(src=resource_manager.Properties.getDefaultOperationFold()):
    log.info("starting rename file job.")
    directorys=os.listdir(src);
    c=0
    for directory in directorys:
        files=subfilesName(src+resource_manager.getSeparator()+directory)
        c+=len(files)
        log.info(str("####"+src+resource_manager.getSeparator()+directory+" directory is doing #### "+str(len(files))))
        path=src+resource_manager.getSeparator()+directory
        i=0;
        for f in files:
            #log.info(os.path.join(f)+"....")
            if os.path.isfile(os.path.join(path,f))==True:
                i=i+1;
                name='{0}_{1:0{2}d}'.format(directory,i,4);
                #log.warn(str(os.path.join(path,f)+" "+ os.path.join(path,name)))
                #os.rename(os.path.join(path,f),os.path.join(path,name));
                #logger.info(f+" --> "+name)
    log.info("finish rename "+str(c)+" job.")