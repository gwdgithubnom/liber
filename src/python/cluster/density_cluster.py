#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import math
from tools import logger
import numpy as np
from pandas import Series, DataFrame
from PIL import Image
# from PIL.Image import core as image
import os, random, string, shutil
from context.resource_manager import Properties

log = logger.getLogger()


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


def chi_function(x):
    """
    to estimate the x value
    whre X(x)=1 if x<0 and X(x)=0 otherwise
    :param x:
    :return:
    """
    if x >= 0:
        return 0
    else:
        return 1


def map_chi_function(x):
    if not isinstance(x, (np.ndarray, np.generic)):
        raise Exception("map chi function type error.")
        log.critical("map chi function type is numpy.float64")
    y = map(chi_function, x)
    y = list(y)
    return y


def rho_function(index_id, distance_ij=np.array([]), distance_c=0):
    """
    to compute the rho_i value
    :param distance_ij:
    :param distance_c: default value=0
    :return:
    """
    row = distance_ij.shape[0]
    distance_c = np.zeros((row, row)) + distance_c
    distance = distance_ij - distance_c
    distance = map(map_chi_function, distance)
    distance = np.array(list(distance))
    # to sum the distance
    distance = np.sum(distance, axis=1)
    rho_id = Series(distance, index=index_id.index)
    return rho_id


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


def delta_function(id_index, index_id, rho_id, distance):
    if not isinstance(rho_id, (np.ndarray, np.generic)) and not isinstance(distance, (np.ndarray, np.generic)):
        raise Exception("rho or distance type error.")
        log.critical("rho distance type is numpy.float64")

    delta_id = Series(id_index.index, index=id_index.values)
    data_id = DataFrame([], columns=['j_id', 'rho', 'delta', 'i', 'j', 'pile'], index=id_index.values)
    data_id['rho'] = rho_id.values
    data_id['i'] = id_index.index
    rho_id = rho_id.sort_values()

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
        i_id = str(id_index[i])
        rho_i = rho_id[i_id]
        order_id = Series(distance[:, i], index=id_index.values)
        # 初始化列表
        # log.debug(order_id.index)
        for j_id in id_index.values:
            j_id = str(j_id)
            # this is log is to record the view the rho_i and rho_j change.
            # s=j+": "+str(rho_index[j])+"  -  " +k+": "+str(rho_i)

            if rho_id[j_id] > rho_i:
                if j_id not in order_id.index:
                    # j=int(index_id[j_id])
                    # log.info(str(j_id)+"  "+str(rho_id[j_id])+" d_ij "+str(distance[i][j]))
                    continue
                # log.warn(str(i_id)+" "+str(rho_i))
                # j=int(index_id[j_id])
                # log.debug(str(j_id)+"  "+str(rho_id[j_id])+" d_ij "+str(distance[i][j]))
                order_id = order_id[order_id <= order_id[j_id]]
                # log.debug(order_id.count())
                # log.debug(order_id)
        try:
            order_id = order_id.sort_values()
        except:
            log.error("search result has something wrong.")
            log.critical(order_id)

        # log.critical(order_id)
        j_id = (order_id.index)[0]
        j = int(index_id[j_id])
        # 构建id  j_id  rho  delta  i  j
        delta_id[i_id] = j_id
        data_id.ix[[i_id], ['j_id']] = j_id
        data_id.ix[[i_id], ['j']] = j
        data_id.ix[[i_id], ['i']] = i
        data_id.ix[[i_id], ['delta']] = distance[i][j]
        # log.debug(str(type(index_id.order_id.index[1])))
        # log.info("i index:"+str(i) +

        # log.debug(str(i)+" time computing,"+" rho_i:"+str(rho_i)+" delta:"+i_id+" j:"+str(order_id.index[1])+" rho_j:"+str(rho_id[j_id])+" distance_ij:"+str(distance[i][j]))

    # this is for the test
    # sys.stdout.write(". ")
    # log.debug("\n"+str(delta_id))
    # data_index['delta']=delta_id.values
    # log.debug("\n"+str(data_index))
    return delta_id, data_id


def init_distance_c(distance):
    mins = list(np.min(np.ma.masked_array(distance, np.isnan(distance)), axis=1))
    mins = np.array(mins)
    min = mins.min()
    # log.warn(min)
    return min


def last_distance_c(maxs, max):
    distance = maxs - max
    # distance = np.extract(distance > 0, distance)
    # distance=np.min(distance[np.nonzero(distance)])
    # log.debug(distance)
    # distance=np.argmin(distance)
    maxs = list(np.max(np.ma.masked_array(distance, np.isnan(distance)), axis=1))
    maxs = np.array(maxs)
    if distance.size > 0:
        # distance = np.max(distance)
        distance = maxs.max()
    else:
        log.critical("error distance_c")
        assert Exception(" no max distance_c.")
    return distance


def get_next_distance_c(mins, min):
    distance = mins - min
    # distance = np.extract(distance > 0, distance)
    # distance=np.min(distance[np.nonzero(distance)])
    # log.debug(distance)
    # distance=np.argmin(distance)
    if distance.size > 0:
        distance = np.min(distance)
    else:
        distance = 0
    return distance


def add_row(df, row):
    colnames = list(df.columns)
    ncol = len(colnames)
    assert ncol == len(row), "Length of row must be the same as width of DataFrame: %s" % row
    return df.append(DataFrame([row], columns=colnames))


def ent_dc(N, threshold, distance, distance_c):
    i = 0
    next_distance_c = get_next_distance_c(distance, distance_c)
    while next_distance_c > 0:
        i = i + 1
        rho = rho_function(distance, distance_c=distance_c)
        rho = rho / N
        e = _calc_ent(rho)
        merge = list([e, distance_c])
        threshold = add_row(threshold, merge)
        distance_c = distance_c + next_distance_c + 1
        next_distance_c = get_next_distance_c(distance, distance_c)
        log.info(str(i) + "time, finished the data about: " + str(distance.shape) + " distance_c:" + str(
            distance_c) + " next increase:" + str(next_distance_c))

    return threshold


"""

def ent_dc_step_by_step(N, threshold, distance, distance_c):
    i = 0
    # next_distance_c=get_next_distance_c(distance,distance_c)
    max_distance_c = last_distance_c(distance, distance_c)
    log.debug("max:"+str(max_distance_c))
    while max_distance_c >= distance_c:
        i = i + 0.5
        rho = rho_function(distance, distance_c=distance_c)
        # log.critical(Series(rho))
        rho = rho / N
        # log.critical(Series(rho))
        e = _calc_ent(rho)
        merge = list([e, distance_c])
        threshold = add_row(threshold, merge)
        # distance_c = distance_c + next_distance_c +1
        distance_c = distance_c + 0.5
        next_distance_c = get_next_distance_c(distance, distance_c)
        log.info(str(i) + "time, finished the data about: " + str(distance.shape) + " distance_c:" + str(
            distance_c) + " next increase:" + str(1))
    return threshold

"""


def find_pile_member(distance, distance_c):
    distance_c = distance - distance_c
    """
     def count():
        i = 0
        while True:
            i += 1
            yield i
    a = count()
    a.__next__()
    """
    # [ c.index for c in distance_c  if c > 0]
    result = []
    i = 0
    for c in distance_c:
        if c <= 0 or np.isnan(c):
            result.append(i)
        i += 1
    # distance_c=[c>0 for c in distance_c ]
    # distance_c=np.sum(distance_c)
    if len(result) > 0:
        return result
    return None


def pile_sub(pile1, pile2):
    """
    对类进行求减法运算
    :param pile1:
    :param pile2:
    :return:
    """
    return list(set(pile1) ^ set(pile2))


def pile_intersection(pile1, pile2):
    """
    对类进行求交集运算
    :param pile1:
    :param pile2:
    :return:
    """
    return list(set(pile1) & set(pile2))


def pile_union(pile1, pile2):
    return list(set(pile1).union(set(pile2)))


def rho_set_tag(id_index, rho_id, pile):
    for p in pile:
        index = id_index[p]
        rho_id[index] = 0
    return rho_id


def pile_function(pile_id, id_index, index_id, data_id, distance, distance_c):
    rho_id = rho_function(index_id, distance, distance_c=distance_c)
    rho_id = rho_id.sort_values(ascending=False)
    # n 多少个需要处理的元素 559
    n = rho_id.shape[0]
    outlier_n=rho_id[(n-1)]
    log.debug(outlier_n)
    if n <= 0:
        # 不存在需要处理的类，返回空DataFrame
        return pile_id
    k = 0
    # 标识类别号，初始化第一个类
    p_id = 1
    i_id = rho_id.index[0]
    # remove the element 标志不用处理
    # 第i个数据点
    i = index_id[i_id]
    pile = find_pile_member(distance[i], distance_c)
    # 对data_id和pile_id表，进行处理标识
    data_id.ix[i_id, 'pile'] = p_id
    # pile_id.ix[p_id,'state'] = pile
    rho_set_tag(id_index, rho_id, pile)
    m = len(pile)
    # add 新行
    # d=d.append(DataFrame([dict(a=a,b=b)],index=[1]))
    if pile is None:
        pile_id = pile_id.append(DataFrame([dict(pile=-1, size=1)], index=index_id.values))
        return None
    pile_id = pile_id.append(DataFrame([dict(pile=pile, size=len(pile), outlier=False)], index=[p_id]))
    # log.debug(pile_id)
    # 标记最下的类标准
    pile_min = len(pile)
    # log.debug("i:"+ str(i))
    # delta_id, data_index = delta_function(id_index, index_id, rho_id, distance)
    while True:
        rho_id = rho_id.sort_values(ascending=False)
        value = rho_id[0]
        if value == 0:
            # 需要处理的元素已经处理完
            break
        outlier = False
        i_id = rho_id.index[0]
        i = index_id[i_id]
        pile = find_pile_member(distance[i], distance_c)

        pile_n = pile_id.shape[0]
        next = 1
        p_id_max = pile_id.shape[0]
        # 假设当前是新类
        p_id = p_id_max + 1
        state = True
        while pile_n >= next:
            # 寻找下一个可能的堆的合并

            pre = pile_id.ix[next, 'pile']
            intersection = pile_intersection(pile, pre)
            if len(intersection) <= 0:
                # 不存在交集的情况
                next += 1
                continue

            elif len(intersection) >= pile_min / 5:
                # 存在交集，而且交集数量已经达到，最小的聚类数
                state = False
                p_id = next
                pile = list(set(pile_union(pile, pre)))
                # log.debug(pile_id)
                pile_id = pile_id.drop(next)
                pile_id = pile_id.append(DataFrame([dict(pile=pile, size=len(pile), outlier=False)], index=[next]))
                # pile_id.ix[next, 'pile']=pile could not add list value to the pile_id
                # 将rho表中进行标记
                # log.warn(rho_id)
                rho_set_tag(id_index, rho_id, pile)
                # log.critical(rho_id)
                next += 1
            else:
                # 存在交集，但数量小于最小聚类数
                pile = list(pile_sub(pile, intersection))
                next += 1
                #设置离群点
                #if len(pile) <= 1:
                if len(pile) <= outlier_n:
                    # 离群点的发现
                    outlier = True
                    break
        if state == True:
            # 对data_id和pile_id表，进行处理标识
            data_id.ix[i_id, 'pile'] = p_id
            m = m + len(pile)
            rho_set_tag(id_index, rho_id, pile)
            pile_id = pile_id.append(DataFrame([dict(pile=pile, size=len(pile), outlier=outlier)], index=[p_id]))
        """
        if pile is None:
            pile_id.ix[p_id, 'size']=0
        else:
            pile_id.ix[p_id, 'size'] = len(pile)
        """
        # log.debug("this is "+str(k)+" times, there has "+str(n-m)+" element has not clustering.")
        k += 1
    log.info("staring computing pile, in distance_c:"+str(distance_c)+". pile count about:"+str(pile_id.shape[0]))
    return pile_id


def ent_dc_step_by_step(id_index, index_id, threshold, distance, distance_c):
    i = 0
    N = int(index_id.shape[0])
    # next_distance_c=get_next_distance_c(distance,distance_c)
    max_distance_c = last_distance_c(distance, distance_c)
    distance_c = distance_c + 1
    log.debug("init the first max distance_c:" + str(max_distance_c))
    while max_distance_c >= distance_c:
        i = i + 0.5
        pile = 0
        # 设置pile的pile元素，与pile的类成员个数
        pile_id = DataFrame([], columns=['pile', 'size', 'outlier'])
        # delta_id, data_id = delta_function(id_index, index_id, rho_id, distance)
        # data = DataFrame([], columns=['gamma', 'rho', 'delta', 'pile'], index=index_id.index)
        data_id = DataFrame([], columns=['j_id', 'rho', 'delta', 'gamma', 'i', 'j', 'pile'], index=id_index.values)
        pile_id = pile_function(pile_id, id_index, index_id, data_id, distance, distance_c)
        pile_size = pile_id['size']
        pile=np.sum(pile_id['outlier'])
        # id_index, index_id
        e = _calc_ent(pile_size.values/N)
        merge = list([e, distance_c,pile])
        threshold = add_row(threshold, merge )
        # distance_c = distance_c + next_distance_c +1
        distance_c = distance_c + 0.5
        next_distance_c = get_next_distance_c(distance, distance_c)
        log.info(str(i) + "time, finished the data about: " + str(distance.shape) + " distance_c:" + str(
            distance_c) + " next increase:" + str(1))
    return threshold


def _calc_ent(probs):
    """
        calculate shanno ent of x

    x_value_list = set([x[i] for i in range(x.shape[0])])
    ent = 0.0
    for x_value in x_value_list:
        p = float(x[x == x_value].shape[0]) / x.shape[0]
        logp = np.log2(p)
        ent -= p * logp

    ent = 0.0
    n=probs.shape[0]
    for i in range(0,n):
        #log.debug("i:"+str(i)+"\t"+str(probs[i]))
        logp=math.log2(probs[i])
        #log.debug("i:"+str(i)+"\t"+str(logp)+"\t"+str(probs[i]))
        ent=ent+logp*probs[i]

    """
    # prob_dict = {x:labels.count(x)/len(labels) for x in labels}

    ent = - probs.dot(np.log2(probs))

    # log.debug("\nx:"+str(i)+"\nlogp:"+str(logp)+"\nent:"+str(ent))
    # log.debug(str(probs)+" \t"+str(ent))


    return ent


def AAcluster():
    # TODO
    return


def binary_array(data):
    # data wuold be modify

    data[data > 200] = 0
    data[data > 0] = 1
    # log.debug(data)
    return data


def cluster(id, data):
    from pandas import Series, DataFrame
    id_index = Series(id.tolist())
    from cluster import density_cluster
    N = id_index.count()
    distance = compute_distance(data)
    distance_c = init_distance_c(distance)
    # id.values -> 对应的key
    index_id = Series(id_index.index, index=id_index.values)
    log.warn("the init distance_c is: " + str(distance_c))
    # to creat the base index table
    # 生成对应的索引，用于控制rho，delta，index的内容
    rho_id = rho_function(index_id, distance, distance_c=distance_c)
    delta_id, data_id = delta_function(id_index, index_id, rho_id, distance)
    # gamma=rho*delta
    threshold = DataFrame([], columns=['H', 'd_c', 'cluster'])
    threshold = ent_dc_step_by_step(id_index, index_id, threshold=threshold, distance=distance, distance_c=distance_c)
    r = threshold
    # log.debug("rho:\n" + str(rho))
    log.debug("threshold\n" + str(DataFrame(threshold)))
    return r

def avery_task(max,min,piece):
    distance=(max-min)/piece
    return distance


def multi_processing_cluster(job,work,df,id, data):
    #threshold = DataFrame([], columns=['H', 'd_c', 'cluster'])
    from pandas import Series, DataFrame
    id_index = Series(id.tolist())
    from cluster import density_cluster
    N = id_index.count()
    distance = compute_distance(data)
    distance_c = init_distance_c(distance)
    # id.values -> 对应的key
    index_id = Series(id_index.index, index=id_index.values)
    log.warn("the init distance_c is: " + str(distance_c))
    # to creat the base index table
    # 生成对应的索引，用于控制rho，delta，index的内容
    rho_id = rho_function(index_id, distance, distance_c=distance_c)
    delta_id, data_id = delta_function(id_index, index_id, rho_id, distance)
    # gamma=rho*delta
    threshold = df
    threshold = ent_dc_step_by_step(id_index, index_id, threshold=threshold, distance=distance, distance_c=distance_c)
    r = threshold
    # log.debug("rho:\n" + str(rho))
    log.debug("worker "+str(work)+" has finished. threshold\n" + str(DataFrame(threshold)))




class BinaryTree:
    def __init__(self, rootObj):
        self.key = rootObj
        self.leftChild = None
        self.rightChild = None

    def insertLeft(self, newNode):
        if self.leftChild == None:
            self.leftChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.leftChild = self.leftChild
            self.leftChild = t

    def insertRight(self, newNode):
        if self.rightChild == None:
            self.rightChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.rightChild = self.rightChild
            self.rightChild = t

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    def setRootVal(self, obj):
        self.key = obj

    def getRootVal(self):
        return self.key
