import os
"""
用于配置常用的初始化信息类
"""
class Properties:


    @classmethod
    def getImageXmlResource(cls):
        """
        返回图像xml文件
        :return:
        """
        return "data/xml/image.xml"

    @classmethod
    def getRootPath(cls):
        """
        返回根目录，路径
        :return:
        """
        path=os.path.dirname(os.path.abspath(__file__))
        path = os.getcwd()
        return path
    @classmethod
    def getDefaultOperationFold(cls):
        """
        返回默认操作目录
        :return:
        """
        file="data/default"
        path=os.path.join(Properties.getRootPath(),file)
        return path

    @classmethod
    def getTestOperationFold(cls):
        """
        返回测试目录
        :return:
        """
        file="data/test"
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
