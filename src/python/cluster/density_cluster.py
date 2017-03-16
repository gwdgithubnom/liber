#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import math
from tools import logger
import numpy as np
from pandas import Series
from PIL import Image
#from PIL.Image import core as image
import os, random, string, shutil
from context.resource_manager import Properties

log = logger.getLogger()

def compute_point_distance(point_i,point_j):
    """
    计算两个点间的距离
    :param point_i:
    :param point_j:
    :return:
    """
    if not isinstance(point_i,(np.ndarray,np.generic)) and not isinstance(point_j,(np.ndarray,np.generic)):
        raise Exception("node type error.")
        log.critical("node type is numpy.float64")

    point_k=(point_i-point_j)*(point_i-point_j)
    return np.sum(point_k)


def chi_function(x):
    """
    to estimate the x value
    whre X(x)=1 if x<0 and X(x)=0 otherwise
    :param x:
    :return:
    """
    if x>=0 :
        return 1
    else:
        return 0

def map_chi_function(x):
    if not isinstance(x,(np.ndarray,np.generic)):
        raise Exception("map chi function type error.")
        log.critical("map chi function type is numpy.float64")
    y=map(chi_function,x)
    y=list(y)
    return y

def rho_function(distance_ij=np.array([]),distance_c=0):
    """
    to compute the rho_i value
    :param distance_ij:
    :param distance_c: default value=0
    :return:
    """
    row=distance_ij.shape[0]
    distance_c=np.zeros((row,row))+distance_c
    distance=distance_ij-distance_c
    distance=map(map_chi_function,distance)
    distance=np.array(list(distance))
    #to sum the distance
    distance=np.sum(distance,axis=1)
    return distance


def compute_distance(data=np.array([])):
    """
    :param data:
    :return:
    the numpy array 按行进行查看
    """
    if data.size <=0:
        raise Exception
        log.critical("cluster need the data, and there has no data in numpy array collection.")
    else:
        log.info("start running compute distance. data count:"+str(data.shape[0])+" point has to computing.")
    row=data.shape[0]
    result=np.zeros((row,row))
    i=0
    for i in range(row):
        j=i
        for j in range(row):
            k=compute_point_distance(data[i],data[j])
            result[i][j]=k;
            result[j][i]=k;
    return result



def delta_function(id_index,index_id,rho_id,distance):
    if not isinstance(rho_id,(np.ndarray,np.generic)) and not isinstance(distance,(np.ndarray,np.generic)):
        raise Exception("rho or distance type error.")
        log.critical("rho distance type is numpy.float64")

    delta_id=Series(id_index.index,index=id_index.values)

    for i in id_index.index:

        # 构建delta的内容
        # to found the best rho_j>rho_i, we may think the k is the i's id value
        i_id=str(id_index[i])
        rho_i=rho_id[i_id]
        order_id=Series(distance[:,i],index=id_index.values)
        #初始化列表
        #log.debug(order_id.index)
        for j_id in id_index.values:
            j_id=str(j_id)
            # this is log is to record the view the rho_i and rho_j change.
            #s=j+": "+str(rho_index[j])+"  -  " +k+": "+str(rho_i)
            #log.debug(s)
            if rho_id[j_id] > rho_i :
                if j_id not in order_id.index:
                    continue
                #log.warn(order_id[j_id])
                order_id=order_id[order_id <= order_id[j_id]]
                #log.debug(order_id)
        try:
            delta_id[i_id]=(order_id.index)[1]
        except:
            log.error("search result has something wrong.")
            log.critical(order_id)
        #log.debug(str(type(index_id.order_id.index[1])))
        #log.info("i index:"+str(i) +
        j_id=(order_id.index)[1]
        j=int(index_id[j_id])
        log.info(str(i)+" time computing,"+" rho_i:"+str(rho_i)+" delta:"+i_id+" j:"+str(order_id.index[1])+" rho_j:"+str(rho_id[j_id])+" distance_ij:"+str(distance[i][j]))

    return delta_id



