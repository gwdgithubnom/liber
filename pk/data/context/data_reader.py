from context.resource_manager import Properties
from pandas import DataFrame, Series
from xml.dom.minidom import parse, parseString
import os
import numpy as np


def conv(o):
    x = np.array(o)
    y = x.astype(np.float)
    return y


class XmlReader:
    def __init__(self, name='default', tag="Data", save=False, relative=True):
        self.name = name
        self.tag = tag

    def getXmlData(self, save=False, relative=True):
        """
        保存id和data数据
        :return:
        """

        if relative:
            path = os.path.join(Properties.getRootPath()+Properties.getXmlLocation() + self.name + ".xml")
        else:
            path = self.name
        images = parse(path)
        id = []
        data = []
        for node in images.getElementsByTagName(self.tag):
            idNode = node.getElementsByTagName("id")[0].childNodes[0].data
            id.append(idNode)
            dataNode = node.getElementsByTagName("data")[0].childNodes[0].data
            dataNode = dataNode[1:-1].split(',')
            data.append(dataNode)
        id = np.asarray(id)
        id = Series(id)
        data = np.asarray(list(map(conv, data)), dtype=np.float)
        if save:
            if not os.path.exists(Properties.getRootPath()+Properties.getDefaultDataFold() + "/cache/" + self.name):
                # f=open(Properties.getDefaultDataFold()+"/csv/threshold.csv","w")
                # f.close()
                os.makedirs(Properties.getRootPath()+Properties.getDefaultDataFold() + "/cache/" + self.name)
            np.save(Properties.getRootPath()+Properties.getRootPath() + "/data/cache/" + self.name + "/id.npy", id)
            np.save(Properties.getRootPath()+Properties.getRootPath() + "/data/cache/" + self.name + "/data.npy", data)

        return id, data

    def loadCacheData(self, name='default', tag="Image", relative=True):
        """
        返回xml数据
        :param name:
        :param tag:
        :param relative:
        :return:
        """

        if relative:
            path = os.path.join(Properties.getRootPath() + "/data/cache/" + name)
        else:
            path = name
        try:
            id = np.load(path + "/id.npy")
            data = np.load(path + "/data.npy")
        except:
            return self.getXmlData(name=name, tag=tag, save=True)
        return id, data


def get_xml_data(name="default", tag="Image"):
    xmlData = XmlReader(name=name, tag=tag, save=False, relative=True)
    return xmlData.getXmlData()


def load_xml_data(name="default", tag="Image"):
    xmlData = XmlReader(name=name, tag=tag, save=False, relative=True)
    return xmlData.loadCacheData()
