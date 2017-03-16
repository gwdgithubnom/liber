#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import math
from tools import logger
import numpy as np
from pandas import Series,DataFrame
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
        return 0
    else:
        return 1

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
        result[i][i]=np.nan

    return result



def delta_function(id_index,index_id,rho_id,distance):
    if not isinstance(rho_id,(np.ndarray,np.generic)) and not isinstance(distance,(np.ndarray,np.generic)):
        raise Exception("rho or distance type error.")
        log.critical("rho distance type is numpy.float64")

    delta_id=Series(id_index.index,index=id_index.values)
    data_index=DataFrame([],columns=['j_id','rho','delta','i','j','threshold'],index=id_index.values)
    data_index['rho']=rho_id.values
    data_index['i']=id_index.index
    rho_id=rho_id.sort_values()

    """
    from view import shape_view
    shape_view.pandas_view_record(distance)
    shape_view.pandas_view_record(rho_id)
    shape_view.pandas_view_record(id_index)
    return
    """
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

            if rho_id[j_id] > rho_i :
                if j_id not in order_id.index:
                    #j=int(index_id[j_id])
                    #log.info(str(j_id)+"  "+str(rho_id[j_id])+" d_ij "+str(distance[i][j]))
                    continue
                #log.warn(str(i_id)+" "+str(rho_i))
                #j=int(index_id[j_id])
                #log.debug(str(j_id)+"  "+str(rho_id[j_id])+" d_ij "+str(distance[i][j]))
                order_id=order_id[order_id <= order_id[j_id]]
                #log.debug(order_id.count())
                #log.debug(order_id)
        try:
            order_id=order_id.sort_values()
        except:
            log.error("search result has something wrong.")
            log.critical(order_id)

        #log.critical(order_id)
        j_id=(order_id.index)[0]
        j=int(index_id[j_id])
        # 构建id  j_id  rho  delta  i  j
        delta_id[i_id]=j_id
        data_index.ix[[i_id],['j_id']]=j_id
        data_index.ix[[i_id],['j']]=j
        data_index.ix[[i_id],['i']]=i
        data_index.ix[[i_id],['delta']]=distance[i][j]
        #log.debug(str(type(index_id.order_id.index[1])))
        #log.info("i index:"+str(i) +

        #log.debug(str(i)+" time computing,"+" rho_i:"+str(rho_i)+" delta:"+i_id+" j:"+str(order_id.index[1])+" rho_j:"+str(rho_id[j_id])+" distance_ij:"+str(distance[i][j]))

    # this is for the test
    #sys.stdout.write(". ")
    #log.debug("\n"+str(delta_id))
    #data_index['delta']=delta_id.values
    #log.debug("\n"+str(data_index))
    return delta_id,data_index


def init_distance_c(distance):
    mins = list(np.min(np.ma.masked_array(distance, np.isnan(distance)), axis=1))
    mins=np.array(mins)
    min=mins.min()
    #log.warn(min)
    return min

def get_next_distance_c(mins,min):
    distance=mins-min
    distance=np.extract(distance>0,distance)
    #distance=np.min(distance[np.nonzero(distance)])
    #log.debug(distance)
    #distance=np.argmin(distance)
    if distance.size>0:
        distance=np.min(distance)
    else:
        distance=0
    return distance


def add_row(df, row):
    colnames = list(df.columns)
    ncol = len(colnames)
    assert ncol == len(row), "Length of row must be the same as width of DataFrame: %s" % row
    return df.append(DataFrame([row], columns=colnames))


def ent_dc(N, threshold, distance, distance_c):
    i=0
    next_distance_c=get_next_distance_c(distance,distance_c)
    while next_distance_c>0 :
        i=i+1
        rho = rho_function(distance,distance_c=distance_c)
        rho = rho/N
        e = _calc_ent(rho)
        merge = list([e,rho])
        threshold = add_row(threshold,merge)
        distance_c = distance_c + next_distance_c +1
        next_distance_c=get_next_distance_c(distance,distance_c)
        log.info(str(i)+"time, finished the data about: "+str(distance.shape)+" distance_c:"+str(distance_c)+" next increase:"+str(next_distance_c))

    return threshold



def _calc_ent(x):
    """
        calculate shanno ent of x
    """
    x_value_list = set([x[i] for i in range(x.shape[0])])
    ent = 0.0
    for x_value in x_value_list:
        p = float(x[x == x_value].shape[0]) / x.shape[0]
        logp = np.log2(p)
        ent -= p * logp
    return ent

def AAcluster():
    #TODO
    return


def cluster(id,data):

    from pandas import Series,DataFrame
    id_index=Series(id.tolist())
    from cluster import density_cluster
    N=id_index.count()
    distance=compute_distance(data)
    distance_c=init_distance_c(distance)

    # id.values -> 对应的key
    index_id=Series(id_index.index,index=id_index.values)
    log.warn("the init distance_c is: "+str(distance_c))
    # to creat the base index table
    # 生成对应的索引，用于控制rho，delta，index的内容

    rho=rho_function(distance,distance_c=distance_c)
    rho_id=Series(rho,index=id)
    delta_id,data_index=delta_function(id_index,index_id,rho_id,distance)
    threshold=DataFrame([],columns=['H','d_c'])

    threshold=ent_dc(N,threshold=threshold,distance=distance,distance_c=distance_c)
    log.debug("rho:\n"+str(rho))
    log.debug("threshold\n"+str(DataFrame(threshold)))