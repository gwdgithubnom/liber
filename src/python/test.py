#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import math
import logging
import logging.config
import numpy as np
from PIL import Image
#from PIL.Image import core as image
import os, random, string, shutil
from scipy import *
from scipy import misc
#logging.basicConfig(level=logging.INFO,format="%(asctime)s %(filename)s[line:%(lineno)d\% (levelname)s %(message)s",datefmt="%Y-%m_%d %H:%M:%S",filename='logs/logger.log',filemode='a')
logging.config.fileConfig("conf/logging.conf")
logger = logging.getLogger("root")
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
    logger.info("PROGRESS: load data")
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
    logger.info("Running compute distance.")
    if not isinstance(node_j,(np.ndarray,np.generic)):
        raise Exception("node type error.")
        logger.critical("node type is numpy.float64")
    n=node_i*node_j
    logger.debug(node_i.shape)


def _test():
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


if __name__ == '__main__':
    #_test()
    a=misc.imread("tools/0.jpg",mode="la")
    b=misc.imread("tools/1.jpg",mode="la")
    logger.debug(a)
    compute_distance(a,b)