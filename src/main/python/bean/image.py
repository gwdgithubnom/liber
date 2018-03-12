from pandas import DataFrame,Series
import numpy as np
import os
from context.resource_manager import Properties
from tools import logger

log=logger.getLogger()

def _conv(o):
    x = np.array(o, dtype='|S4')
    y = x.astype(np.float)
    return y


def get_data_from_xml(path=Properties.getImageXmlResource()):
    """
    解析xml文件，获得对应的id，data，作为运算的基础
    :param path:
    :return: list, NumpArray  用于显示控制与用于计算
    list is used to make the index to location the value
    """
    log.info("starting running compute_distance_from_xml function.")
    from context.resource_manager import Properties
    from pandas import DataFrame,Series
    path=os.path.join(Properties.getRootPath(),Properties.getImageXmlResource())
    from xml.dom.minidom import parse,parseString
    images=parse(path)
    id=[]
    data=[]
    for node in images.getElementsByTagName("Image"):
        idNode=node.getElementsByTagName("id")[0].childNodes[0].data
        id.append(idNode)
        dataNode=node.getElementsByTagName("data")[0].childNodes[0].data
        dataNode=dataNode[1:-1].split(',')
        data.append(dataNode)
    id=np.asarray(id)
    id=id.tolist()
    data=np.asarray(data)
    data=np.asarray(list(map(_conv,data)),dtype=np.float)
    return id,data



class Image:
    def __init__(self):
          self.id=""
          self.data=""