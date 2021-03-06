#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import math
from tools import logger
import numpy as np
from PIL import Image
# from PIL.Image import core as image
import os, random, string, shutil
from scipy import *
from scipy import misc
from pandas import DataFrame as df

# logging.basicConfig(level=logging.INFO,format="%(asctime)s %(filename)s[line:%(lineno)d\% (levelname)s %(message)s",datefmt="%Y-%m_%d %H:%M:%S",filename='logs/logger.log',filemode='a')


log = logger.getLogger();
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


def compute_distance(node_i=[], node_j=[]):
    """
    npArray数据类型计算
    :param node_i:
    :param node_j:
    :return:
    """
    log.info("Running compute distance.")
    if not isinstance(node_j, (np.ndarray, np.generic)):
        raise Exception("node type error.")
        log.critical("node type is numpy.float64")
    n = node_i * node_j
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
    misc.imsave("tools/test.jpg",f)
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
    a = misc.imread("tools/0.jpg", mode="L")
    b = misc.imread("tools/1.jpg", mode="L")
    a = np.array(a, np.float64)
    b = np.array(b, np.float64)
    from cluster import density_cluster
    c = density_cluster.compute_point_distance(a, b)
    from view import shape_view
    shape_view.numpy_view(c, state="record")
    log.debug(np.sum(c))


def conv(o):
    x = np.array(o)
    y = x.astype(np.float)
    return y


"""

"""


def add_row(df, row):
    colnames = list(df.columns)
    ncol = len(colnames)
    from pandas import DataFrame
    assert ncol == len(row), "Length of row must be the same as width of DataFrame: %s" % row
    return df.append(DataFrame([row], columns=colnames))


def save():
    from context.resource_manager import Properties
    from pandas import DataFrame, Series
    path = os.path.join(Properties.getRootPath(), Properties.getImageXmlResource())
    from xml.dom.minidom import parse, parseString
    images = parse(path)
    id = []
    data = []
    for node in images.getElementsByTagName("Image"):
        idNode = node.getElementsByTagName("id")[0].childNodes[0].data
        id.append(idNode)
        dataNode = node.getElementsByTagName("data")[0].childNodes[0].data
        dataNode = dataNode[1:-1].split(',')
        data.append(dataNode)
    id = np.asarray(id)
    id = Series(id)
    data = np.asarray(list(map(conv, data)), dtype=np.float)
    np.save(Properties.getRootPath() + "/data/cache/id.npy", id)
    np.save(Properties.getRootPath() + "/data/cache/data.npy", data)


def add_row(df, row):
    colnames = list(df.columns)
    ncol = len(colnames)
    assert ncol == len(row), "Length of row must be the same as width of DataFrame: %s" % row
    return df.append(DataFrame([row], columns=colnames))


def distance_view(m, index_id, id_index, distance):
    max = distance.shape[0]
    d = DataFrame([], columns=['i_id', 'j_id', 'i', 'j', 'value'])
    m = index_id[m]
    for i in range(m, m + 1):
        for j in range(i, max):
            l = []
            l.append(id_index[i])
            l.append(id_index[j])
            l.append(i)
            l.append(j)
            l.append(distance[i][j])
            print(l)

    return d


def cluster_distance_view(m, index_id, id_index, distance, distance_c):
    max = distance.shape[0]
    d = DataFrame([], columns=['i_id', 'j_id', 'i', 'j', 'value'])
    m = index_id[m]
    for i in range(m, m + 1):
        for j in range(0, max):
            if distance[i][j] <= distance_c:
                l = []
                l.append(id_index[i])
                l.append(id_index[j])
                l.append(i)
                l.append(j)
                l.append(distance[i][j])
                print(l)

    return d


if __name__ == '__main__':
    """
from cluster import density_cluster
    from pandas import Series,DataFrame
    from context.resource_manager import Properties
    from view import shape_view
    from cluster import density_cluster
    id=np.load(Properties.getRootPath()+"/data/cache/id.npy")
    data=np.load(Properties.getRootPath()+"/data/cache/data.npy")
    id_index=Series(id.tolist())
    from cluster.density_cluster import *
    N=id_index.count()
    distance=compute_distance(data)
    distance_c=init_distance_c(distance)
    shape_view.pandas_view_record(list(distance))
    # id.values -> 对应的key
    index_id=Series(id_index.index,index=id_index.values)
    log.warn("the init distance_c is: "+str(distance_c))
    log.debug(distance_c)
    # to creat the base index table
    # 生成对应的索引，用于控制rho，delta，index的内容
    log.debug(distance)
    rho=rho_function(distance,distance_c=3021276)

    rho_id=Series(rho,index=id)
    log.critical(rho)
    """
    from cluster import density_cluster
    from pandas import Series
    from pandas import Series, DataFrame
    from context.resource_manager import Properties
    from view import shape_view
    from cluster import density_cluster

    name = 'path'
    distance_c = 12.3972318748
    m = '3_44'
    pile = 0
    id = np.load(Properties.getRootPath() + "/data/cache/" + name + "/id.npy")
    data = np.load(Properties.getRootPath() + "/data/cache/" + name + "/data.npy")
    id_index = Series(id.tolist())
    from cluster import density_cluster
    index_id = Series(id_index.index, index=id_index.values)
    distance = density_cluster.compute_distance(data)
    pile_id = DataFrame([], columns=['pile', 'size'])
    rho_id = density_cluster.rho_function(index_id, distance, distance_c=distance_c)
    rho_id = Series(rho_id, index=index_id.index)
    rho_id = rho_id.sort_values(ascending=False)
    #delta_id, data_id = density_cluster.delta_function(id_index, index_id, rho_id, distance)
    log.debug(rho_id)
    pile=['3_44']
    pile_max=14
    pile = density_cluster.pile_brother(index_id, id_index, distance, distance_c, pile,pile_max)
    log.debug("pile info:")
    log.debug(pile)
    distance_view(m, index_id, id_index, distance)
    log.debug("cluster_view: " + str(rho_id[index_id[m]]))
    cluster_distance_view(m, index_id, id_index, distance, distance_c)

    """
    import numpy
    import multiprocessing
       d = DataFrame([], columns=['i_id', 'j_id', 'i', 'j', 'value'])
    pool = multiprocessing.Pool(processes=20)
    result = list(range(20))
    for i in range(20):
        pool.apply_async(distance_view, (d,i, index_id, id_index, distance))
        # d = numpy.concatenate([c, c], axis=0)
    pool.close()
    pool.join()
    log.debug(d)

    rho_id = density_cluster.rho_function(index_id,distance, distance_c=distance_c)
    data = DataFrame([], columns=['gamma','rho','delta','pile'],index=index_id.index)
    delta_id, data_index = density_cluster.delta_function(id_index, index_id, rho_id, distance)
    density_cluster.pile_function(pile_id,id_index,index_id,rho_id,distance)
    #TODO
    #id_index, index_id
    log.critical(str(pile_id)+"\npile:"+pile)
    """
