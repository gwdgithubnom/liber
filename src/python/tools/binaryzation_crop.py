import os
import sys
from PIL import Image
#from PIL.Image import core as image
import os, random, string, shutil
import time
from  tools import logger
from context import resource_manager
log=logger.getLogger()
"""
    walk through a directory and get all the file in this directory.
"""


class BinAndCrop():

    def __init__(self, path='data/pic.jpg'):
        self.path = path


    def checkPath(self,toPath="data/"):
        self.toPath = toPath
        self.state = os.path.exists(toPath)
        if self.state == False:
            os.makedirs(toPath)
            log.info("check the bin directory is exist:" + str(self.state) + " and mkdir path:" + toPath)
        else:
            log.info("check the bin directory is exist:" + str(self.state))

    def binary(self):
        img = Image.open(self.path)
        img = img.convert("L")
        img = img.resize((126, 126), Image.ANTIALIAS)
        new_name = self.path[:24] + '_binary'
        img.save(new_name, "JPEG")
        os.remove(self.path)


    def single_bin(self,filename=""):
        if filename == "":
            log.warning("user should define the file location.")
            return;
        img = Image.open(filename)
        img = img.convert("L")
        img.save(filename,"jpeg")
        log.info(filename+" has finished binary.")

    def bincrop(self):
        img = Image.open(self.path)
        img = img.convert("L")
        i=resource_manager.Properties.getImageDefaultSize()
        img = img.resize((i,i), Image.ANTIALIAS)
        new_name = self.path[:24] + '_bincrop'
        test_name= self.toPath+self.timename()
        log.info("size:"+i+"*"+i+" ,save file " + self.toPath + self.timename() + ".jpg")
        img.save(test_name+".jpg","JPEG")
        img.save(new_name, "JPEG")
        os.remove(self.path)

    def timename(self):
        return str(time.time())

    def logtime(self):
        return time.strftime("%Y-%m-%d %H:%M %p", time.localtime())
