from PIL import Image
import os
from numpy import genfromtxt
import gzip, pickle
from glob import glob
import numpy as np
import pandas as pd
from  tools import logger
import theano
from context import resource_manager
from tools import file_manage

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
    Blue = '\34[95m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def dir_to_dataset(glob_files):
    dataset = []
    clazz = []
    for file_count, file_name in enumerate(sorted(glob(glob_files), key=len)):
        log.info(file_name + "Working process:\n\t %s" % glob_files)
        image = Image.open(file_name)
        img = Image.open(file_name).convert('LA')  # tograyscale
        pixels = [f[0] for f in list(img.getdata())]
        dataset.append(pixels)
        classLabel = file_name.split("_")[1];
        print
        file_name, "<--->", classLabel
        clazz.append(classLabel)
        if file_count % 1000 == 0:
            print("\t %s files processed" % file_count)
    # outfile = glob_files+"out"
    # np.save(outfile, dataset)

    return np.array(dataset), np.array(clazz)


def build_proxy(path):
    s = path.split(resource_manager.getSeparator())
    s = s[(len(s) - 1)]
    c = 0
    if s[0:4] == "data":
        log.info(" do binaryzation about files in " + str(path))
        size = s[4:]
        size = int(size)
        for i in os.walk(path, False):
            for f in i[2]:
                c = c + 1
        return c
    return 0


def initDataSet(src=resource_manager.Properties.getDefaultWorkFold()):
    log.info("starting to build image cnn pkz file.")
    # print "start binaryzationJpg()"
    files = file_manage.subdirs(src)
    # files=file_manage.subfilesName(path);
    # print "###########",src,"##",length,"###########"
    sizeSet=set()
    for f in files:
        path = os.path.join(src, f)
        if os.path.isdir(path):
            # shutil.copy(os.path.join(path,f),os.path.join(path,f))

            s =path.split(resource_manager.getSeparator())
            s = s[(len(s) - 1)]
            c = 0
            size = 0
            if s[0:4] == "data":
                log.info(" do binaryzation about files in " + str(path))
                size = s[4:]
                size = str(size)
                sizeSet.add(size)
            else:
                continue
    for size in sizeSet:
        path = resource_manager.Properties.getDefaultWorkFold()+"train/data" + size + "/*";
        Data, y = dir_to_dataset(path)
        # Data and labels are read

        train_set_x = np.asarray(Data, dtype=theano.config.floatX);
        train_set_y = y;

        path = resource_manager.Properties.getDefaultWorkFold()+"verify/data" + size + "/*";
        Data, y = dir_to_dataset(path)

        val_set_x = np.asarray(Data, dtype=theano.config.floatX);
        val_set_y = y

        path = resource_manager.Properties.getDefaultWorkFold()+"test/data" + size + "/*";
        Data, y = dir_to_dataset(path)

        test_set_x = np.asarray(Data, dtype=theano.config.floatX);
        test_set_y = y

        train_set = train_set_x, train_set_y
        val_set = val_set_x, val_set_y
        test_set = test_set_x, test_set_y
        dataset = [train_set, val_set, test_set]
        log.info("staring build pkl file ......")
        name = resource_manager.Properties.getDefaultDataFold()+'pickle/file-' + size + '.pkl.gz';
        f = gzip.open(name, 'wb')
        pickle.dump(dataset, f, protocol=2)
        f.close()
        log.info("the file of file-"+size+".pkl.gz file has been created at " + resource_manager.Properties.getDefaultDataFold() + "pickle" + "....")


# this is to test the data
def testData(index):
    f = gzip.open('file-28.pkl.gz', 'rb')
    train_set, valid_set, test_set = pickle.load(f)
    train_set_x = train_set[0];
    train_set_y = train_set[1];
    sample = np.asarray(train_set_x, dtype=theano.config.floatX)
    print
    len(sample[0])
    a = sample[index]
    j = 0;
    for i in range(0, len(a)):
        if a[i] > 128:
            print
            pcolors.FAIL + "*",
        else:
            print
            pcolors.HEADER + "0",
        if ((i + 1) % 28 == 0):
            print
            ""
    print
    "label is:%s" % train_set_y[index]

if __name__=="__main__":
    initDataSet(src=resource_manager.Properties.getDefaultWorkFold())
