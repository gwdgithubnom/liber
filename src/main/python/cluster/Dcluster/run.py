# -*- coding: utf-8 -*-
import numpy as np
from numpy.linalg import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from .mds import mds
from .readfile import readfile
from .rhodelta import rhodelta
from .DCplot import DCplot
from context import resource_manager
from tools import  logger
log=logger.getLogger()

def run(file=resource_manager.Properties.getDefaultDataFold()+"module"+resource_manager.getSeparator()+"distance.txt",sep=' '):
    '''
    return cluster id
    '''
    (dist,xxdist,ND,N) = readfile(file, dimensions = 2, sep=sep)
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

if __name__=="__main__":
    from context.resource_manager import Properties
    from pandas import Series
    from view import shape_view
    from view import plot_utils
    from cluster import density_cluster
    name='flame'
    id = np.load(Properties.getRootPath() + "/data/cache/" + name + "/id.npy")
    data = np.load(Properties.getRootPath() + "/data/cache/" + name + "/data.npy")
    id_index = Series(id.tolist())
    from cluster import density_cluster
    N = id_index.count()
    distance = compute_distance(data)
    # id.values -> 对应的key
    index_id = Series(id_index.index, index=id_index.values)
    log.warn("the init distance_c is: " + str(distance_c))
