import os, random, string, shutil
from tools import logger
from tools import logger
from context import resource_manager
from tools import  file_manage
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
def initDirs(path):
    filelist = []
    if not os.path.exists(path):
        os.makedirs(path)
    filelist = os.listdir(path)
    for f in filelist:
        filepath = os.path.join(path, f)
        if os.path.isfile(filepath):
            os.remove(filepath)
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath, True)
        os.makedirs(filepath)

def start_image_rename(src=resource_manager.Properties.getDefaultOperationFold(),
                       path=resource_manager.Properties.getDefaultWorkFold(),state=True):
    if state:
        log.info("starting to rename file in dir, do not modify the resource path file. Operation Directory:"+str(path))
        dirs = file_manage.subdirs(src)
        c=0
        if os.path.exists(path):
            shutil.rmtree(path)
        if len(dirs)>0:
            for d in dirs:
                files = file_manage.subfilesName(d)
                for f in files:
                    name = file_manage.random_str(8) + "_" + f
                    try:
                        shutil.copy(os.path.join(d, f), os.path.join(path+resource_manager.getSeparator()+d, name))
                    except:
                        file_manage.fix_path(path+resource_manager.getSeparator()+d)
                        shutil.copy(os.path.join(d, f), os.path.join(path+resource_manager.getSeparator()+d, name))
                    c=c+1
        log.info("finished copy file to the path"+str(path)+". about "+str(c)+" files.")
        file_manage.rename_files(path)
    else:
        log.info("starting to rename file in dir, modify the resource path file. Operation Directory:"+str(src))
        file_manage.rename_files(path)


def start_image_rebuild(src=resource_manager.Properties.getDefaultOperationFold(),
                        path=resource_manager.Properties.getDefaultWorkFold(),target=['data28','data100'],train=70,verify=30,test=30,state=False):

    log.info("starting to separtion work. rebuild the image directory. At " + src)
    # path=raw_input("src path:");
    # 	#n=raw_input("input train mount decimals:");
    # m=raw_input("input verify mount decimals:");
    # l=raw_input("input ssdfdssdf mout decimals:");
    if state:
        log.info("please input the train,verify,test factor:")
        train = int(input())
        verify = int(input())
        test = int(input())

    train = train * 0.01
    verify = verify * 0.01
    test = test * 0.01

    log.info("this is the factor:"+str(train) + ","+str(verify)+ ","+str(test))
    i = 0;
    dirs = file_manage.subdirs(src)
    dpath = path + "train"
    # print dpath;
    initDirs(dpath)
    dpath = path + "verify"
    initDirs(dpath)
    dpath = path + "test"
    initDirs(dpath)
    c=0
    if os.path.exists(path):
        shutil.rmtree(path)
    if len(dirs)>0:
        for d in dirs:
            # files = os.listdir(src)
            files = file_manage.subfilesName(d)
            length = len(files)
            # print "###########",d,"###########"
            i = 1;
            for f in files:
                name = file_manage.random_str(8) + "_" + f
                if i <= length * train:
                    p = path + "train"
                elif i <= (length * train + length * verify):
                    p = path + "verify"
                else:
                    p = path + "test"
                try:
                    for t in target:
                        shutil.copy(os.path.join(d, f), os.path.join(p +resource_manager.getSeparator()+t, name))
                except:
                    for t in target:
                        file_manage.fix_path(p + resource_manager.getSeparator()+ t)
                        shutil.copy(os.path.join(d, f), os.path.join(p +resource_manager.getSeparator()+ t, name))
                # os.rename(os.path(join(d,f),os.path.join(p+"/data100",name);
                i = i + 1
                c=c+1
            # print i,":",d," file:",f,"--->",p," file:",name
    else:
        d=src
        files = file_manage.subfilesName(d)
        length=len(files)
        for f in files:
            name = file_manage.random_str(8) + "_" + f
            if i <= length * train:
                p = path + "train"
            elif i <= (length * train + length * verify):
                p = path + "verify"
            else:
                p = path + "test"
            try:
                for t in target:
                    shutil.copy(os.path.join(d, f), os.path.join(p +resource_manager.getSeparator()+t, name))
            except:
                for t in target:
                    file_manage.fix_path(p +resource_manager.getSeparator()+ t)
                    shutil.copy(os.path.join(d, f), os.path.join(p +resource_manager.getSeparator()+ t, name))
            # os.rename(os.path(join(d,f),os.path.join(p+"/data100",name);
            i = i + 1
            c=c+1
    log.info("finished copy file to the path"+str(path)+". about "+str(c)+" files.")
    file_manage.renamefiles(path)


def usage():
    """
    The output  configuration file contents.

    Usage: config.py [-d|--domain,[number|'m']] [-c|--cache,[allow|deny]] [-h|--help] [-v|--version] [output, =[argument]]

    Description
                -d,--domain Generate domain configuration,take 13 or 19 number,"m" is the second - tier cities.
                -c,--cache  Configure cache policy. "allow" or "deny".
                -h,--help    Display help information.
                -v,--version  Display version number.
    for example:
        python config.py -d 13
        python config.py -c allow
        python config.py -h
        python config.py -d 13 -c allow
    """


if __name__=="__main__":
    """
    首先允许image_build 生成图像，binarzation，dataset_build
    """
    import sys
    import getopt
    try:
        opts,args=getopt.getopt(sys.argv[1:], "hl:t:p:")
        l=[]
        p=['default']
        for op, value in opts:
            if op=="-l":
                p=value
            elif op=="-t":
                s=value.split(',')
                l=s
            elif op=="-p":
                s=value.split(',')
                train=int(s[0])
                verify=int(s[1])
                test=int(s[2])
            elif op=='-h':
                print(usage().__doc__)
                exit()
    except getopt.error as msg:
        log.info(msg)
        log.error("need input location and target size.")
        log.info("for help use --help")
        exit
    #start_image_rebuild(src=resource_manager.Properties.getDefaultDataFold()+"/yiwen/size200/",path=resource_manager.Properties.getDefaultWorkFold(),target=['data28','data52'])
    #log.info("path:"+str(p)+"\ttarget:"+type(l))
    start_image_rebuild(src=resource_manager.Properties.getDefaultDataFold()+p,path=resource_manager.Properties.getDefaultWorkFold(),target=l,train=train,verify=verify,test=test)