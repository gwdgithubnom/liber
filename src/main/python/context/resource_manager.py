import os
import platform
import  time
"""
用于配置常用的初始化信息类
"""
def getSeparator():
    """
    if 'Windows' in platform.system():
        separator = '\\'
    else:
        separator = '/'
    :return:
    """
    separator=os.path.sep
    return separator

def findPath(file):
    """
    to locate the root path.
    :param file:
    :return:
    """
    o_path = os.getcwd()
    separator = getSeparator()
    str = o_path
    str = str.split(separator)
    while len(str) > 0:
        spath = separator.join(str)+separator+file
        leng = len(str)
        if os.path.exists(spath):
            return spath
        str.remove(str[leng-1])

class Properties:

    timename=time.strftime("%Y-%m-%d-%H-%M", time.localtime())

    @classmethod
    def name_str_YMD(self):
        return time.strftime("%Y-%m-%d", time.localtime())

    @classmethod
    def name_str_static(self):
        return Properties.timename

    @classmethod
    def getImageXmlResource(cls):
        """
        返回图像xml文件
        :return:
        """
        return "data/xml/image.xml"

    @classmethod
    def getXmlLocation(cls):
        """
        返回图像xml文件
        :return:
        """
        return "data/xml/"

    @classmethod
    def getRootPath(cls):
        """
        返回根目录，路径
        :return:
        """
        #path=os.path.dirname(os.path.abspath(__file__))
        #path = os.getcwd()
        path = findPath("python")
        os.chdir(path)
        return path+"/"
    @classmethod
    def getDefaultOperationFold(cls):
        """
        返回默认操作目录
        :return:
        """
        file="data/default/"
        path=os.path.join(Properties.getRootPath(),file)
        return path

    @classmethod
    def getDefaultDataFold(cls):
        """
        返回默认操作目录
        :return:
        """
        file="data/"
        path=os.path.join(Properties.getRootPath(),file)
        return path

    @classmethod
    def getDefaultWorkFold(cls):
        """
        返回默认操作目录
        :return:
        """
        s=Properties.getRootPath()
        s="/home/gwd/Projects/"
        file="data/work/"
        path=os.path.join(s,file)
        return path

    @classmethod
    def getTestOperationFold(cls):
        """
        返回测试目录
        :return:
        """
        file="data/ssdfdssdf/"
        path=os.path.join(Properties.getRootPath(),file)
        return path

    @classmethod
    def getDirectoryConfigPath(cls):
        """
        返回目录配置文件
        :return:
        """

        file="conf/directory.ini"
        path=os.path.join(Properties.getRootPath(),file)
        return path

    @classmethod
    def getImageDefaultSize(cls):
        """
        返回图像默认大小
        :return:
        """
        size=100
        return size

    @classmethod
    def getImageDefaultFileLocation(cls):
        path='data/pic.jpg'
        return os.path.join(Properties.getRootPath(),path)

    @classmethod
    def getBlackImageLocation(cls):
        path='data/black.jpg'
        return os.path.join(Properties.getRootPath(),path)

    @classmethod
    def getWhiteImageLocation(cls):
        path="data/white.jpg"
        return os.path.join(Properties.getRootPath(),path)

