from PIL import Image
from xml.dom import minidom
from pandas import Series
from numpy import genfromtxt
# import gzip, cPickle for this is used simple
import gzip
import _pickle as cPickle
#
# for nickname cPickle because pickle has replase cPickle in pandans
import pickle as cPickle
import pickle
from glob import glob
import numpy as np
import os
#import theano
import xml.etree.ElementTree
from conda.config import subdir
class pcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    Blue='\34[95m'
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def dir_to_dataset(path):
    print("Gonna process:\n\t %s"%path)
    dataset = []
    #for file_count, file_name in enumerate( sorted(glob(glob_files),key=len) ):
    subdir=os.listdir(path)
    for dir in subdir:
        if os.path.isdir(os.path.join(path,dir)):
            print("start read director "+os.path.join(path,dir))
            dataset.extend(dir_to_dataset(os.path.join(path,dir))) 
        elif os.path.isfile(os.path.join(path,dir)):
                filename=os.path.join(path,dir)      
                print("read file:"+filename)
                #image = Image.open(dir)
                img = Image.open(filename).convert('LA') #tograyscale
                pixels = [f[0] for f in list(img.getdata())]
                filename=os.path.basename(dir)
                #print(filename[0:-4])
                #pixels.append(int(filename[0:-4]))
                pixels.insert(0,(filename[0:-4]))
                dataset.append(pixels)
    return dataset
"""
for this method update at 20160913 to add new code to support to create image.xml
http://www.cnblogs.com/wangshide/archive/2011/10/29/2228936.html
http://www.cnblogs.com/xiaowuyi/archive/2012/10/17/2727912.html
http://www.cnblogs.com/coser/archive/2012/01/10/2318298.html
"""
def initDataSet():
    #path="D:\Projects\\Python\\deeplay\\src\\train\\run\\*";
    path="./train/run"
    Data= dir_to_dataset(path)
    Data=np.array(Data)
    # Data and labels are read
    #set a filename
    afileName = str(os.getcwd()) + "\\kmeans.data"
    #create the file
    file = open(afileName, 'w')
    #put the data into a file.
    print(len(Data))
    xmlFile=str(os.getcwd())+"\\image1.xml"

    if(os.path.exists(xmlFile)==False):
         document=minidom.Document()
         document.appendChild(document.createComment("this is used for save a image file"))
         imagelist=document.createElement("Images")
         document.appendChild(imagelist)
         f=open("image.xml","w")
         document.writexml(f,addindent=' '*4, newl='\n', encoding='utf-8')
         f.close()
    root=xml.dom.minidom.parse('image.xml')
    imagesRoot=root.documentElement
    #root=xml.etree.ElementTree.parse("image.xml");

    for x in range(0, len(Data)):
        imageRoot=document.createElement("Image")
        id=document.createElement("id")
        data=document.createElement("data")
        aRow = Data[x]
        value=[]
        for pix in range(1, len(aRow)):
            file.write(str(aRow[pix]))
            value.append(int(str(aRow[pix])))
            if pix != len(aRow) - 1:
                file.write(",")
        #print(len(aRow))
        id.appendChild(document.createTextNode(aRow[0]))
        data.appendChild(document.createTextNode(str(value)))
        imagesRoot.appendChild(imageRoot)
        imageRoot.appendChild(id)
        imageRoot.appendChild(data)
        file.write("\n")
    f=open("image.xml","w")
    root.writexml(f,addindent=' '*4, newl='\n', encoding='utf-8')
    f.close()

def rmfile(xmlFile=str(os.getcwd())+"\\image.xml"):
    try:
        os.remove(xmlFile)
    except:
        print("not found file "+xmlFile)

#run
rmfile()
initDataSet()
