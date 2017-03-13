#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import math
from tools import logger
import numpy as np
from PIL import Image
#from PIL.Image import core as image
import os, random, string, shutil
from scipy import *
from scipy import misc
from pandas import DataFrame as df
#logging.basicConfig(level=logging.INFO,format="%(asctime)s %(filename)s[line:%(lineno)d\% (levelname)s %(message)s",datefmt="%Y-%m_%d %H:%M:%S",filename='logs/logger.log',filemode='a')


log=logger.getLogger();
"""
logger.info("abc")
logger.debug("debug")
logger.warn("warn")
logger.debug("debug")
logger.warning("warning")
logger.error("error")
logger.critical("critical")
"""
def load_paperdata(distance_f):
    '''
    Load distance from data

    Args:
        distance_f : distance file, the format is column1-index 1, column2-index 2, column3-distance

    Returns:
        distances dict, max distance, min distance, max continues id
    '''
    log.info("PROGRESS: load data")
    distances = {}
    min_dis, max_dis = sys.float_info.max, 0.0
    max_id = 0
    with open(distance_f, 'r') as fp:
        for line in fp:
            x1, x2, d = line.strip().split(' ')
            x1, x2 = int(x1), int(x2)
            max_id = max(max_id, x1, x2)
            dis = float(d)
            min_dis, max_dis = min(min_dis, dis), max(max_dis, dis)
            distances[(x1, x2)] = float(d)
            distances[(x2, x1)] = float(d)
    for i in range(max_id):
        distances[(i, i)] = 0.0
    logger.info("PROGRESS: load end")
    return distances, max_dis, min_dis, max_id

def compute_distance(node_i=[],node_j=[]):
    """
    npArray数据类型计算
    :param node_i:
    :param node_j:
    :return:
    """
    log.info("Running compute distance.")
    if not isinstance(node_j,(np.ndarray,np.generic)):
        raise Exception("node type error.")
        log.critical("node type is numpy.float64")
    n=node_i*node_j
    logger.debug(node_i.shape)


def _test():
    """
     from PIL import Image
    img = Image.open("tools/0.jpg")
    img = img.convert("L")
    pixdata = img.load()
    print(img)
    rows = img.size[0]
    cols = img.size[1]
    logging.debug("abc")
    f=misc.face()
    misc.imsave("tools/3.jpg",f)
    s=misc.imread("tools/0.jpg")
    from scipy import linalg
    print(linalg.det(s))
    print(s.shape)
    import matplotlib.pyplot as plt
    plt.imshow(s)
    plt.show()
    file="tools/0.jpg"
    from tools.binaryzation_crop import *
    BinAndCrop().single_bin(filename=file)
    a=misc.imread("tools/0.jpg",mode="L")
    b=misc.imread("tools/1.jpg",mode="L")
    np.set_printoptions(threshold=nan)
    logger.debug(a)
    c=np.arange(1024)
    from view import shape_view
    from pandas import *
    d=DataFrame(c)
    f=DataFrame(a[0:60,0:50])
    s=a
    import matplotlib.pyplot as plt
    plt.imshow(s)
    plt.show()
    shape_view.numpy_view(f,state="record")
    compute_distance(a,b)
    :return:
    """
    from tools import binaryzation_crop
    log.debug("start running ...")
    a=misc.imread("tools/0.jpg",mode="L")
    b=misc.imread("tools/1.jpg",mode="L")
    a=np.array(a,np.float64)
    b=np.array(b,np.float64)
    from cluster import density_cluster
    c=density_cluster.compute_point_distance(a,b)
    from view import shape_view
    shape_view.numpy_view(c,state="record")
    log.debug(np.sum(c))




if __name__ == '__main__':
    from context.resource_manager import Properties
    path=os.path.join(Properties.getRootPath(),Properties.getImageXmlResource())
    from xml.dom.minidom import parse,parseString
    images=parse(path)
    id=[]
    data=[]
    for node in images.getElementById("Image"):
        for subNode in node.childNodes:
            idNode=subNode.getElmentsByTagName("id")
            dataNode=subNode.getElmentsByTagName("data")


