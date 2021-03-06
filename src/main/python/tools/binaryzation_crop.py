import os
import sys
from PIL import Image
#from PIL.Image import core as image
import os, random, string, shutil
import time
from  tools import logger
from context import resource_manager
from tools import file_manage
from view import plot_utils
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

    def binary(self,size=resource_manager.Properties.getImageDefaultSize()):
        img = Image.open(self.path)
        img = img.convert("L")
        img = img.resize((size, size), Image.ANTIALIAS)
        new_name = self.path[:24] + '_binary'
        img.save(new_name, "JPEG")
        os.remove(self.path)


    @classmethod
    def single_binary(cls,filename=""):
        """
        无对象处理方式
        :param filename:
        :return:
        """
        if filename == "":
            log.warning("user should define the file location.")
            return;
        img = Image.open(filename)
        img = img.convert("L")
        img.save(filename,"jpeg")
        log.info(filename+" has finished binary.")

    @classmethod
    def timename(cls):
        """
        自动生成时间名称
        :return:
        """
        return str(time.time())

    def logtime(self):
        return time.strftime("%Y-%m-%d %H:%M %p", time.localtime())

    @classmethod
    def single_binary_crop(cls,path=resource_manager.Properties.getDefaultOperationFold(),size=resource_manager.Properties.getImageDefaultSize()):
            """
            无对象处理方式，并实现截图
            :param size:
            :return:
            """
            img = Image.open(path)
            img = img.convert("LA")
            img = img.resize((size,size), Image.ANTIALIAS)
            new_name = path[:24] + '_bincrop'
            test_name= path+BinAndCrop.timename()
            log.info("size:"+size+"*"+size+" ,save file " + test_name + ".jpg")
            img.save(test_name+".jpg","JPEG")
            img.save(new_name, "JPEG")
            os.remove(path)



    @classmethod
    def single_crop(cls,fileName=resource_manager.Properties.getImageDefaultFileLocation(),size=resource_manager.Properties.getImageDefaultSize()):
            """
            图像进行裁剪
            :return:
            """
            #print "Processing ... ", fileName
            #open the image
            try:
                img = Image.open(fileName)
                img=img.resize((size,size),Image.ANTIALIAS);
                img.save(fileName, "JPEG")
            except:
                log.warn("for "+fileName+"file could not open or resize error.")

    @classmethod
    def crop(cls, fileName=resource_manager.Properties.getImageDefaultFileLocation(),
                    size=resource_manager.Properties.getImageDefaultSize()):
        """
        图像进行裁剪
        :return:
        """
        # print "Processing ... ", fileName
        # open the image
        img = Image.open(fileName)
        img = img.resize((size, size), Image.ANTIALIAS);
        img.save(fileName, "JPEG")


    @classmethod
    def preOp(cls,fileName=resource_manager.Properties.getDefaultOperationFold()):
            #print "Processing ... ", fileName
            if fileName == '':
                return
                #only process the jpg file
            #    sufix = os.path.splitext(fileName)[1][1:]
            #    if sufix != 'jpg':
            #        return

            #load background
            backGround = Image.open(resource_manager.Properties.getBlackImageLocation())
            backGround = backGround.convert('RGBA')

            #print fileName;
            #open the image
            #img = Image.open(fileName)
            #img = img.covert("RGB")
            img=backGround
            try:
                img = Image.open(fileName)
                # img = img.convert("LA")
                img = img.convert("RGB")
            except:
                os.remove(fileName)
                log.warn("wrong file in this directory "+fileName+". and delete the file.")
                exit
            pixdata = img.load()
            rows=img.size[0];
            cols=img.size[1];
            #scan by cols
            """
            for y in range(cols):
                for x in range(rows):
                    pixdata[x,y]=0  if pixdata[x,y]>=128 else 255
            """
            for width_x in range(img.size[0]):
                for height_y in range(img.size[1]):
                    pixel = img.getpixel((width_x, height_y))
                    # print('start' + str(img.getpixel((width_x, height_y))))
                    gray = pixel[0] * 0.299 + pixel[1] * 0.587 + pixel[2] * 0.114
                    if (gray < 140):
                        pixel = (0, 0, 0)
                    else:
                        pixel = (255, 255, 255)
                    # z = (255 - z) / 255 * 255
                    img.putpixel((width_x, height_y), pixel)

            #crop the image to 100 * 100
            if rows != 100 and cols != 100:
                box = (0,0, rows,cols)
                region = img.crop(box)
                positioin = (int((100-rows)/2), int((100-cols)/2), int((100-rows)/2+rows), int((100-cols)/2+cols) )
                #print positioin
                backGround.paste(region,positioin)
                img = backGround
            # plot_utils.plot_image_file(img)
            #print "......#####",fileName,"######....."
            img.save(fileName, "JPEG")

    @classmethod
    def binaryzation_proxy(cls,path):
        s = path.split(resource_manager.getSeparator())
        s = s[(len(s) - 1)]
        c=0

        if s[0:4]=="data":
            log.info(" do binaryzation about files in "+str(path))
            size=s[4:]
            size=int(size)
            for i in os.walk(path, False):
                for f in i[2]:
                    BinAndCrop.preOp(os.path.join(path, f));
                    BinAndCrop.single_crop(path+resource_manager.getSeparator()+f,size)
                    c=c+1
            return c
        return 0

    @classmethod
    def binaryzation_image(cls,path=resource_manager.Properties.getDefaultOperationFold()):
            """
            图像预处理接口
            :return:
            """
            log.info("starting to running binaryzation image working.")
            # print "start binaryzationJpg()"
            files=file_manage.subdirs(path)
            # files=file_manage.subfilesName(path);
            #print "###########",src,"##",length,"###########"
            i=1;
            for f in files:
                if os.path.isdir(os.path.join(path,f)):
                    # shutil.copy(os.path.join(path,f),os.path.join(path,f))
                    i=i+BinAndCrop.binaryzation_proxy(os.path.join(path,f))
            log.info("About "+str(i)+" files has binaryzay....")

def binaryzation(path=resource_manager.Properties.getDefaultOperationFold()):
    log.info("starting to binary the image fold:"+path)
    BinAndCrop.binaryzation_image(path)

if __name__=="__main__":
    path=resource_manager.Properties.getDefaultWorkFold()
    binaryzation(path)