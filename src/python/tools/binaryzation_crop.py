import os
import sys
from PIL import Image
#from PIL.Image import core as image
import os, random, string, shutil
import time
import logging
import logging.config
logging.config.fileConfig("conf/logging.conf")
logger = logging.getLogger("root")
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
            logger.info("check the bin directory is exist:" + str(self.state) + " and mkdir path:" + toPath)
        else:
            logger.info("check the bin directory is exist:" + str(self.state))

    def binary(self):
        img = Image.open(self.path)
        img = img.convert("L")
        img = img.resize((126, 126), Image.ANTIALIAS)
        new_name = self.path[:24] + '_binary'
        img.save(new_name, "JPEG")
        os.remove(self.path)

    def bincrop(self):
        img = Image.open(self.path)
        img = img.convert("L")
        img = img.resize((126, 126), Image.ANTIALIAS)
        new_name = self.path[:24] + '_bincrop'
        test_name= self.toPath+self.timename()
        logger.info(" save file " + self.toPath + self.timename() + ".jpg")
        img.save(test_name+".jpg","JPEG")
        img.save(new_name, "JPEG")
        os.remove(self.path)

    def timename(self):
        return str(time.time())

    def logtime(self):
        return time.strftime("%Y-%m-%d %H:%M %p", time.localtime())
