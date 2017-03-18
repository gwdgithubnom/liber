import os, random, string, shutil
from tools import logger
from tools import logger
from context import resource_manager

log = logger.getLogger()

"""
def rename():
	for f in files:
		if os.path.isfile(os.path.join(path,f))==True:
			i=i+1;
			name='{0}_{1:0{2}d}'.format(prefix,i,4);
			os.rename(os.path.join(path,f),os.path.join(path,name));
		# f,"-->",name

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


def initDirs(path):
    filelist = []
    filelist = os.listdir(path)
    for f in filelist:
        filepath = os.path.join(path, f)
        if os.path.isfile(filepath):
            os.remove(filepath)
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath, True)
        os.makedirs(filepath)


def start_image_rebuild(src=resource_manager.Properties.getDefaultOperationFold(),
                        path=resource_manager.Properties.getDefaultWorkFold(), train=0, verify=0, test=0, state=False):
    log.info("starting to separtion work. rebuild the image directory. At " + src)
    # path=raw_input("src path:");
    # 	#n=raw_input("input train mount decimals:");
    # m=raw_input("input verify mount decimals:");
    # l=raw_input("input test mout decimals:");
    if state:
        log.info("please input the train,verify,test factor:")
        train = input()
        verify = input()
        test = input()
    train = train * 0.01
    verify = verify * 0.01
    test = test * 0.01
    # train=train*0.01;
    # verify=verify*0.01;
    # test=test*0.01;
    if train > 0:
        log.info("this is the factor:", train, ",", verify, ",", test)
        files = os.listdir(src)
        i = 0;
        dirs = subdirs(src)
        dpath = path + "/train"
        # print dpath;
        initDirs(dpath)
        dpath = path + "/verify"
        initDirs(dpath)
        dpath = path + "/test"
        initDirs(dpath)
        for d in dirs:
            files = subfilesName(d)
            length = len(files)
            # print "###########",d,"###########"
            i = 1;
            for f in files:
                name = random_str(8) + "_" + f
                if i <= length * train:
                    p = path + "/train"
                elif i <= (length * train + length * verify):
                    p = path + "/verify"
                else:
                    p = path + "/test"
                shutil.copy(os.path.join(d, f), os.path.join(p + "/data100", name))
                shutil.copy(os.path.join(d, f), os.path.join(p + "/data28", name))
                # os.rename(os.path(join(d,f),os.path.join(p+"/data100",name);
                i = i + 1
            # print i,":",d," file:",f,"--->",p," file:",name
    else:
        log.info("starting to rebuild file in dir.")
