# -*- coding: utf-8 -*-
import numpy as np
from numpy.linalg import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from mds import mds
from readfile import readfile
from rhodelta import rhodelta
from DCplot import DCplot
from context import resource_manager
from tools import  logger
import os
log=logger.getLogger()

def run(path=resource_manager.Properties.getDefaultDataFold()+"txt"+resource_manager.getSeparator()+"build.txt",sep=' '):
    '''
    return cluster id
    i,j distance
    '''
    (dist,xxdist,ND,N) = readfile(path, dimensions = 2, sep=sep)
    XY, eigs = mds(dist)
    (rho,delta,ordrho,dc,nneigh) = rhodelta(dist, xxdist, ND, N, percent = 2.0)
    DCplot(dist, XY, ND, rho, delta,ordrho,dc,nneigh,17,0.1)

def compute_point_distance(point_i, point_j):
    """
    计算两个点间的距离
    :param point_i:
    :param point_j:
    :return:
    """
    if not isinstance(point_i, (np.ndarray, np.generic)) and not isinstance(point_j, (np.ndarray, np.generic)):
        raise Exception("node type error.")
        log.critical("node type is numpy.float64")

    point_k = (point_i - point_j) * (point_i - point_j)
    return np.sum(point_k)

def compute_distance(data=np.array([])):
    """
    :param data:
    :return:
    the numpy array 按行进行查看
    """
    if data.size <= 0:
        raise Exception
        log.critical("cluster need the data, and there has no data in numpy array collection.")
    else:
        log.info("start running compute distance. data count:" + str(data.shape[0]) + " point has to computing.")
    row = data.shape[0]
    result = np.zeros((row, row))
    i = 0
    for i in range(row):
        j = i
        for j in range(row):
            k = compute_point_distance(data[i], data[j])
            result[i][j] = k;
            result[j][i] = k;
        result[i][i] = np.nan

    return result
def build_distance_txt(distance,sep=' ',path=resource_manager.Properties.getDefaultDataFold()+"txt"+resource_manager.getSeparator()+"build.txt"):
    """
    写入文件，具体格式如下：
    行下标 分隔符 列下标 分隔符 distance中行下标和列下标对应的值
    :param distance:
    :param path:
    :param sep:分隔符
    :return:
    """
    num_row=0
    num_rank=0
    fr= open(path, 'w')
    for row in distance:
        num_row += 1
        num_rank = 0
        for element in row:
            if np.isnan(element):
                continue
            num_rank += 1
            fr.write(str(num_row))
            fr.write(sep)
            fr.write(str(num_rank))
            fr.write(sep)
            fr.write(str(element))
            fr.write("\n")
    fr.close()
    """
    i =distance.shape[0]
    j = distance.shape[1]
    log.debug(distance)
    for ii in range(1,i):
        for jj in range(i,j):
            fr.write(str(ii))
            fr.write(sep)
            fr.write(str(jj))
            fr.write(sep)
            fr.write(str(distance[ii,jj]))
            fr.write("\n")
        fr.flush()
    
    
    """



def conv(o):
    x = np.array(o)
    y = x.astype(np.float)
    return y

def save(name='default'):
    """
    保存id和data数据
    :return:
    """
    from context.resource_manager import Properties
    from pandas import DataFrame, Series
    path = os.path.join(Properties.getDefaultDataFold()+"xml"+resource_manager.getSeparator()+name+".xml")
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
    if not os.path.exists(Properties.getDefaultDataFold()+"/cache/"+name):
        #f=open(Properties.getDefaultDataFold()+"/csv/threshold.csv","w")
        #f.close()
        os.makedirs(Properties.getDefaultDataFold()+"/cache/"+name)
    np.save(Properties.getRootPath() + "/data/cache/"+name+"/id.npy", id)
    np.save(Properties.getRootPath() + "/data/cache/"+name+"/data.npy", data)



if __name__=="__main__":
    from context.resource_manager import Properties
    from pandas import Series
    from view import shape_view
    from view import plot_utils
    from cluster import density_cluster
    distance_c=0.69
    name='aggregation'
    save(name)
    id = np.load(Properties.getRootPath() + "/data/cache/" + name + "/id.npy")
    data = np.load(Properties.getRootPath() + "/data/cache/" + name + "/data.npy")
    path =resource_manager.Properties.getDefaultDataFold()+"txt"+resource_manager.getSeparator()+"build.txt"
    id_index = Series(id.tolist())
    from cluster import density_cluster
    N = id_index.count()
    distance = compute_distance(data)
    build_distance_txt(distance)
    # id.values -> 对应的key
    run(path)
    log.warn("the init distance_c is: " + str(distance_c))
