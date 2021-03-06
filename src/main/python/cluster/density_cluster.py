#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# python -m cProfile -s cumulative main.py
import sys
import os
import math
import pandas
from tools import logger
import numpy as np
from pandas import Series, DataFrame
from PIL import Image
# from PIL.Image import core as image
import os, random, string, shutil
from context.resource_manager import Properties
from scipy import stats

log = logger.getLogger()


def compute_point_distance(point_i, point_j):
    """
    计算两个点间的距离

    :param point_i:
    :param point_j:
    :return: 返回两点的距离值
    """
    if not isinstance(point_i, (np.ndarray, np.generic)) and not isinstance(point_j, (np.ndarray, np.generic)):
        raise Exception("node type error.")
        log.critical("node type is numpy.float64")

    point_k = (point_i - point_j) * (point_i - point_j)
    return np.sum(point_k)


def chi_function(x):
    """
    to estimate the x value
    评估函数，返回评估价值1或为0
    whre X(x)=1 if x<0 and X(x)=0 otherwise
    :param x:
    :return:
    """
    if x >= 0:
        return 0
    else:
        return 1


def map_chi_function(x):
    """
    用于map的函数计算
    :param x:
    :return:
    """
    if not isinstance(x, (np.ndarray, np.generic)):
        raise Exception("map chi function type error.")
        log.critical("map chi function type is numpy.float64")
    y = map(chi_function, x)
    y = list(y)
    return y


def delta_function(id_index, rho_id, distance):
    """
    评估类之间距离，主要根据rho_id
    center_id
    :param id_index:
    :param index_id:
    :param rho_id:
    :param distance:
    :return:
    """
    if not isinstance(rho_id, (np.ndarray, np.generic)) and not isinstance(distance, (np.ndarray, np.generic)):
        raise Exception("rho or distance type error.")
        log.critical("rho distance type is numpy.float64")
    delta_id = Series(id_index.index.copy(True), index=id_index.values)
    # data_id = DataFrame([], columns=['i_id', 'j_id', 'rho', 'delta', 'gamma', 'i', 'j', 'pile'],                        index=id_index.values)
    # data_id['rho'] = rho_id.values
    # data_id['i'] = id_index.index
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
        # j = int(index_id[j_id])
        # 构建id  j_id  rho  delta  i  j
        delta_id[i_id] = j_id
        # data_id.ix[[i_id], ['j_id']] = j_id
        # data_id.ix[[i_id], ['j']] = j
        # data_id.ix[[i_id], ['i']] = i
        # data_id.ix[[i_id], ['i_id']] = i_id
        # data_id.ix[[i_id], ['delta']] = distance[i][j]
        # data_id.ix[[i_id], ['rho']] = rho_id[i_id]
        # data_id.ix[[i_id], ['gamma']] = rho_id[i_id] * distance[i][j]
        # log.debug(str(type(index_id.order_id.index[1])))
        # log.info("i index:"+str(i) +

        # log.debug(str(i)+" time computing,"+" rho_i:"+str(rho_i)+" delta:"+i_id+" j:"+str(order_id.index[1])+" rho_j:"+str(rho_id[j_id])+" distance_ij:"+str(distance[i][j]))

    # this is for the ssdfdssdf
    # sys.stdout.write(". ")
    # log.debug("\n"+str(delta_id))
    # data_index['delta']=delta_id.values
    # log.debug("\n"+str(data_index))

    return delta_id


def delta_random_function(rho_id, delta_id, pile, i_id):
    for i in pile:
        if i == i_id:
            # log.debug("delta parent:" + str(i))
            continue
        elif rho_id[delta_id[i]] > rho_id[delta_id[i_id]]:
            delta_id[i] = i_id
    return delta_id


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
    rho_id = Series(distance, index=index_id.index.copy(True))
    return rho_id


def rho_max(pile, rho_id):
    """
    返回最大的rho值，与所对应的密度中心点
    :param pile:
    :param rho_id:
    :return:
    """
    if len(pile) <= 0:
        return 0
    index = pile[0]
    max = rho_id[0]
    for i in pile:
        if rho_id[i] > max:
            max = rho_id[i]
            index = i
    return max, index


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
    np.save(Properties.getRootPath() + "/data/cache/distance/data.npy", result)
    return result


def min_distance(distance):
    """
    返回最小的距离值
    :param distance:
    :return:
    """
    mins = list(np.min(np.ma.masked_array(distance, np.isnan(distance)), axis=1))
    mins = np.array(mins)
    min = mins.min()
    # log.warn(min)
    return min


def max_distance(maxs, max):
    """
    返回最大的distance距离值
    :param maxs:
    :param max:
    :return:
    """
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
    """
    获取下一个最小距离值的增长点
    :param mins:
    :param min:
    :return:
    """
    distance = mins - min
    distance = np.extract(distance > 0, distance)
    distance = distance[np.nonzero(distance)]
    if distance.size > 0:
        distance = np.min(distance)
    else:
        distance = 0
    # log.debug(distance)
    # distance=np.argmin(distance)

    return distance


def add_row(df, row):
    """
    添加一行DataFrame记录
    :param df:
    :param row:
    :return:
    """
    colnames = list(df.columns)
    ncol = len(colnames)
    assert ncol == len(row), "Length of row must be the same as width of DataFrame: %s" % row
    return df.append(DataFrame([row], columns=colnames))


def ent_dc(N, threshold, distance, distance_c):
    """
    信息熵……………………
    :param N:
    :param threshold:
    :param distance:
    :param distance_c:
    :return:
    """
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


def find_pile_member(id_index, distance, distance_c):
    """
    乱码？
    寻找在一定的distance_c下的聚类
    :param distance:
    :param distance_c:
    :return:
    """
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
            id = id_index[i]
            result.append(id)
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
    return list(set(pile1) - set(pile2))


def pile_intersection(pile1, pile2):
    """
    对类进行求交集运算
    :param pile1:
    :param pile2:
    :return:
    """
    #return list(set(pile1) & set(pile2))
    return list(set(pile1).intersection(set(pile2)))

def pile_union(pile1, pile2):
    return list(set(pile1).union(set(pile2)))


def rho_set_tag(rho_id, pile):
    for p in pile:
        rho_id[p] = 0
    return rho_id


def pile_brother(index_id, id_index, distance, distance_c, pile, rho_id, threshold, state=False):
    pre = 0
    next_pile = pile
    while len(pile) != pre:
        pre = len(pile)
        pile_next = []
        next_pile = sorted(next_pile, key=lambda v: rho_id[v], reverse=True)
        for l in next_pile:
            l = index_id[l]
            p = find_pile_member(id_index, distance[l], distance_c)
            b = pile_union(pile, p)
            if len(b) >= threshold:
                pile_next.extend(pile_sub(p, pile))
                if state:
                    break
        next_pile = pile_next
        pile = list(set(pile_union(pile, pile_next)))
    pile = sorted(pile, key=lambda v: rho_id[v], reverse=True)
    return pile


def pile_children(index_id, id_index, distance, distance_c, pile, rho_id, delta_id, state=False):
    pre = 0
    next_pile = pile
    while len(pile) != pre:
        pre = len(pile)
        pile_next = []
        # next_pile.sort(key=lambda v:rho_id[v],reverse=True)
        next_pile = sorted(next_pile, key=lambda v: rho_id[v], reverse=True)
        last = 0
        for l in next_pile:
            ll = index_id[l]
            p = find_pile_member(id_index, distance[ll], distance_c)
            delta_id = delta_random_function(rho_id, delta_id, p, l)
            last = (rho_id[delta_id[l]] + last) / 2
            s = str(rho_id[delta_id[l]]) + "/" + delta_id[l]
            if len(p) <= rho_id[delta_id[l]]:
                lll = pile_sub(p, pile)
                pile_next.extend(lll)
                if state:
                    break

        next_pile = pile_next
        pile = list(set(pile_union(pile, pile_next)))
    pile = sorted(pile, key=lambda v: rho_id[v], reverse=True)
    return pile, delta_id


def numpy_find_min(data, base):
    """
    求解的编号，所以需要减去一
    :param data:
    :param base:
    :return:
    """
    data[np.isnan(data)] = base + np.max(data)
    base = np.argmin(data)
    return base - 1


def outlier_to_pile(outlier, index_id, id_index, distance, distance_c, next_distance_c, border, pile_id, rho_id,
                    threshold):
    # TODO to merge pile
    pile_id = pile_id.sort_values('size', ascending=False)
    pile_id = pile_id.reset_index(drop=True)
    pile_id_size = len(pile_id)
    state = False
    temp = distance_c
    jarge_state = True
    while True:
        pile = pile_brother(index_id, id_index, distance, temp, outlier, rho_id, threshold, state=True)
        # if len(pile)>pile_min:
        jarge_point = []
        jarge_point_next = []
        jarge_size = threshold

        for ii in range(pile_id_size):
            jarge_pile = pile_id.ix[ii, 'pile']
            jarge = pile_intersection(jarge_pile, pile)
            if len(jarge) >= jarge_size :
                jarge_point.append(ii)
                jarge_size = len(jarge)
                state = True
            elif len(jarge) > 0 and jarge_state and not state:
                jarge_point_next.append(ii)
            else:
                continue

        if len(jarge_point_next) > 0:
            jarge_state = False

        if state:
            max = jarge_point[0]
            for ii in jarge_point:
                if len(pile_id.ix[ii, 'pile']) > len(pile_id.ix[max, 'pile']):
                    max = ii
            pile = pile_union(outlier, pile_id.loc[max, 'pile'])
            # pile_id.ix[max,'pile']=pile
            pile_id.set_value(max, 'pile', pile)
            pile_id.set_value(max, 'size', len(pile))
            pile = []
            break
        # log.debug(str(c)+" "+str(temp+border)+"/"+str(temp))
        elif temp >= border:
            # pile_id = pile_id.append(DataFrame([dict(pile=pile, p_id=-1, size=len(pile), outlier=True)], index=[len(pile_id)]))
            """
            while  len(outlier) != 0:

                item=outlier.pop()
                index_item=index_id[item]
                d=distance[index_item]
                log.debug(d)
                j=numpy_find_min(d,distance_c)
                jj=d[j]
                jjjj=id_index[j]
                jjjjj=distance[index_item,index_id[jjjj]]

            """
            if len(jarge_point_next) > 0:
                max = jarge_point_next[0]
                for ii in jarge_point_next:
                    if len(pile_id.ix[ii, 'pile']) > len(pile_id.ix[max, 'pile']):
                        max = ii
                pile = pile_union(outlier, pile_id.loc[max, 'pile'])
                # pile_id.ix[max,'pile']=pile
                pile_id.set_value(max, 'pile', pile)
                pile_id.set_value(max, 'size', len(pile))
                pile = []
            else:
                pile_id = pile_id.append(
                    DataFrame([dict(pile=outlier, p_id=-1, size=len(outlier), outlier=True)], index=[len(pile_id)]))
            break
        temp = temp + next_distance_c
    return pile_id


def pile_to_pile(pile1, pile2, rho_id):
    rho1, index1 = rho_max(pile1, rho_id)
    rho2, index2 = rho_max(pile2.rho_id)
    if rho1 >= rho2:
        return pile_union(pile1, pile2), True
    else:
        return pile1, False


def pile_check(data, dataset, level, index_id, id_index, distance, distance_c,rho_id, delta_id, pile_id, threshold):
    pile_id = pile_id.sort_values('size', ascending=False)
    pile_id = pile_id.reset_index(drop=True)
    log.info("running pile debug check..")
    state=False
    i=0
    while len(pile_id)>i:
        check = pile_id.loc[i, 'pile']
        outlier = pile_id.loc[i,'outlier']
        pile_id = pile_id.drop(i)
        pile_id = pile_id.sort_values('size', ascending=False)
        pile_id = pile_id.reset_index(drop=True)
        #p1, delta_id = pile_children(index_id, id_index, distance, distance_c, check, rho_id, delta_id)
        p1=pile_brother(index_id, id_index, distance, distance_c, check, rho_id, threshold, state=True)
        j=0
        while len(pile_id)>j:
            pre = pile_id.loc[j, 'pile']
            p2=pile_brother(index_id, id_index, distance, distance_c, pre, rho_id, threshold, state=True)
            intersection = pile_intersection(p1, p2)

            if len(intersection) > threshold or len(intersection)>=len(check) or len(intersection)>=len(pre):
                check = list(set(pile_union(check, pre)))
                outlier=False
                p1=pile_brother(index_id, id_index, distance, distance_c, check, rho_id, threshold, state=True)
                pile_id = pile_id.drop(j)
                pile_id = pile_id.reset_index(drop=True)
                i=0
                j=0
                state=True
            j+=1
        pile_id = pile_id.append(
            DataFrame([dict(pile=check, p_id=len(pile_id), size=len(check), outlier=outlier)]),ignore_index=True)
        pile_id = pile_id.sort_values('size', ascending=False)
        pile_id = pile_id.reset_index(drop=True)
        i+=1

    save_show_cluster(index_id, data, distance_c, pile_id, dataset=dataset, level="DEBUG",
                      level_info="final merge pile")
    return pile_id, delta_id


def debug_pile_check(data, dataset, level, index_id, id_index, distance, distance_c, rho_id, delta_id, pile_id,
                     threshold):
    pile_id = pile_id.sort_values('size', ascending=False)
    pile_id = pile_id.reset_index(drop=True)
    log.info("running pile debug check..")
    state=False
    i=0
    import time
    while len(pile_id)>i:
        check = pile_id.loc[i, 'pile']
        outlier=pile_id.loc[i,'outlier']
        pile_id = pile_id.drop(i)
        pile_id = pile_id.sort_values('size', ascending=False)
        pile_id = pile_id.reset_index(drop=True)
        #p1, delta_id = pile_children(index_id, id_index, distance, distance_c, check, rho_id, delta_id)
        p1=pile_brother(index_id, id_index, distance, distance_c, check, rho_id, threshold, state=True)
        j=0
        while len(pile_id)>j:
            pre = pile_id.loc[j, 'pile']
            log.debug(time.time())
            log.warn("---- aaa --- "+str(j)+"\t"+str(len(p1)))
            p2=pile_brother(index_id, id_index, distance, distance_c, pre, rho_id, threshold, state=True)
            log.warn("bbb "+str(len(p2)))
            intersection = pile_intersection(p1, p2)
            log.warn("ccc "+str(len(pile_id))+"\t"+str(len(intersection)))
            if len(intersection) > threshold or len(intersection)>=len(check) or len(intersection)>=len(pre):
                check = list(set(pile_union(check, pre)))
                p1=pile_brother(index_id, id_index, distance, distance_c, check, rho_id, threshold, state=True)
                pile_id = pile_id.drop(j)
                pile_id = pile_id.reset_index(drop=True)
                outlier=False
                i=0
                j=0
                state=True
            j+=1
            log.warn("ddd "+str(i)+"\t"+str(len(p1)))
            log.debug(time.time())

        pile_id = pile_id.append(
            DataFrame([dict(pile=check, p_id=len(pile_id), size=len(check), outlier=outlier)]),ignore_index=True)
        pile_id = pile_id.sort_values('size', ascending=False)
        pile_id = pile_id.reset_index(drop=True)
        if  state:
            save_show_cluster(index_id, data, distance_c, pile_id, dataset=dataset, level="DEBUG",
                          level_info="merge pile")
        i+=1
        log.debug(pile_id)
    save_show_cluster(index_id, data, distance_c, pile_id, dataset=dataset, level="DEBUG",
                      level_info="final merge pile")
    return pile_id, delta_id

def pile_rho_values(pile,rho_id,rho_id_border,rho_id_border_mean,rho_id_border_ava):
    sort_value=0
    for l in pile:
        sort_value=rho_id[l]+rho_id_border[l]*0.8+rho_id_border_ava[l]*0.8+rho_id_border_mean[l]*0.8*0.8*0.8
    return  sort_value


def pile_function(pile_id, id_index, index_id, data, distance, distance_c, next_distance_c, dataset="default",
                  level="INFO"):
    # 初始化队列
    log.info("staring running pile_function.. distance_c:"+str(distance_c)+" dataset:"+dataset)
    rho_id = rho_function(index_id, distance, distance_c=distance_c)
    delta_id = Series(rho_id.index.copy(deep=True), index=rho_id.index.copy(deep=True))
    # 局部边界，用于设置视角
    temp = distance.copy()
    temp[np.isnan(temp)] = 0
    stand = np.std(temp)
    temp = distance.copy()
    cache=temp.ravel()
    temp[np.isnan(temp)] = stand
    # temp=temp.mid(axis=0)
    # next_distance_c=np.std(temp)
    temp = np.min(temp, axis=0)
    border_mean=np.mean(temp,axis=0)
    border = np.max(temp)
    percent = 2.0
    position = int(index_id.shape[0] * (index_id.shape[0] + 1) / 2 * percent / 100)
    border_ava = sorted(cache)[position * 2 + index_id.shape[0]]

    rho_id_border_ava=rho_function(index_id,distance,distance_c=border_ava)

    rho_id_border=rho_function(index_id, distance, distance_c=border)
    rho_id_border_mean=rho_function(index_id, distance, distance_c=border_mean)
    # delta_id, data_id = delta_function(id_index, index_id, rho_id, distance)
    # 队列进行重排续
    rho_id = rho_id.sort_values(ascending=False)
    rho_id_tag = rho_id.copy(deep=True)
    # n 多少个需要处理的元素 559
    n = rho_id.shape[0]
    if n <= 0:
        # 不存在需要处理的类，返回空DataFrame
        return pile_id

    # 标记最下的类标准
    # 取得最小的聚类聚类标准，通过求非1的最小值
    pile_max = rho_id.mean()
    # pile_max = stats.gmean(rho_id.values)
    pile_min = get_next_distance_c(rho_id, 1)
    if pile_min > pile_max:
        pile_min = math.floor(pile_max)
    pile_max = math.ceil(pile_max)
    # pile_min = 3
    # 初始化二级队列
    inlier_list = []
    outlier_list = []
    k = 0
    # 标识类别号，初始化第一个类
    p_id = 1
    i_id = rho_id.index[0]
    # remove the element 标志不用处理
    # 第i个数据点
    i = index_id[i_id]
    # bug，pile的顺序
    pile = find_pile_member(id_index, distance[i], distance_c)
    # log.debug((str(len(pile))+"   %%%%%   "+str(pile)))
    # pile.sort(key=lambda v:rho_id[v],reverse=True)
    # pile=sorted(pile,key=lambda v:rho_id[v])
    delta_id = delta_random_function(rho_id, delta_id, pile, i_id)
    pile, delta_id = pile_children(index_id, id_index, distance, distance_c, pile, rho_id, delta_id)
    # pile.sort(key=lambda v:rho_id[v],reverse=True)
    # pile=sorted(pile,key=lambda v:rho_id[v])
    # log.debug((str(len(pile))+"   %%%%%   "+str(pile)))
    # 对data_id和pile_id表，进行处理标识
    # data_id.ix[i_id, 'pile'] = p_id
    # pile_id.ix[p_id,'state'] = pile
    rho_set_tag(rho_id_tag, pile)
    # m = len(pile)
    # add 新行
    # d=d.append(DataFrame([dict(a=a,b=b)],index=[1]))
    if pile is None:
        # pile_id = pile_id.append(DataFrame([dict(pile=-1, size=1)], index=index_id.values))
        return None
    pile_id = pile_id.append(DataFrame([dict(p_id=p_id, pile=pile, size=len(pile), outlier=False)], index=[p_id]))
    # log.debug(pile_id)
    # log.debug("i:"+ str(i))
    # delta_id, data_index = delta_function(id_index, index_id, rho_id, distance)
    static_distance_c = distance_c
    while True:
        # log.debug(pile_id)

        rho_id_tag = rho_id_tag.sort_values(ascending=False)
        pile_id = pile_id.reset_index(drop=True)
        value = rho_id_tag[0]
        if value == 0:
            # 控制是否进行无离群点考虑
            # pile_id=pile_to_pile(outlier_list,index_id, id_index, distance, distance_c, pile_id, pile_min)
            log.info("do job on outliers")
            outlier_list = []
            pile_id_size = len(pile_id)
            outlier_list_temp = []
            for ii in range(pile_id_size):
                if pile_id.loc[ii, 'size'] >= pile_max or not pile_id.loc[ii, 'outlier']:
                    continue
                elif pile_id.loc[ii, 'outlier']:
                    pile_id_pile = pile_id.ix[ii, 'pile']
                    pile_id = pile_id.drop(ii)
                    # if len(pile_id_pile) == 1:
                    #     outlier_list_temp.extend(pile_id_pile)
                    # else:
                    #     outlier_list.append(pile_id_pile)
                    outlier_list.append(pile_id_pile)

            pile_id = pile_id.reset_index(drop=True)
            # i=0
            o_o = []

            outlier_list = sorted(outlier_list, key=lambda v: pile_rho_values(v,rho_id,rho_id_border,rho_id_border_mean,rho_id_border_ava), reverse=True)

            # for l in outlier_list:
            #     log.debug(str(l)+"\n"+str(pile_rho_values(l,rho_id,rho_id_border,rho_id_border_mean))+"\t"+str(rho_id_border_mean[l])+"\t"+str(rho_id[l])+"\t"+str(rho_id_border_mean[l]))
            # exit(1)

            for ll in outlier_list:
                # 以pile_min进行评估收敛性
                pile_id = outlier_to_pile(ll, index_id, id_index, distance, distance_c, next_distance_c, border,
                                          pile_id, rho_id,
                                          pile_max)
                if level is "DEBUG":
                    save_show_cluster(index_id, data, distance_c, pile_id, dataset=dataset, level=level,
                                      level_info="merge outlier")

                i = i + 1
            # pile_id = pile_id.append(DataFrame([dict(pile=pile, p_id=-1, size=len(pile), outlier=True)], index=[p_id]))
            if level is not "INFO":
                pile_id, delta_id = debug_pile_check(data, dataset, level, index_id, id_index, distance, border_ava,rho_id, delta_id, pile_id, pile_max)
            else:
                pile_id, delta_id = pile_check(data, dataset, level, index_id, id_index, distance, border_ava,rho_id, delta_id, pile_id, pile_max)

            save_show_cluster(index_id, data, distance_c, pile_id, dataset=dataset, level=level,
                                  level_info="final result")
            break

        elif value <= pile_min:
            # rho_set_tag( rho_id_tag, pile)
            i_id = rho_id_tag.index[0]
            rho_id_tag[i_id] = 0
            # 当前是噪声

            if value==pile_max:
                pile_id = pile_id.append(DataFrame([dict(pile=[i_id], p_id=p_id, size=len(pile), outlier=False)], index=[len(pile_id)]))
            else:
                pile_id = pile_id.append(DataFrame([dict(pile=[i_id], p_id=p_id, size=len(pile), outlier=True)], index=[len(pile_id)]))

            pile_id = pile_id.reset_index(drop=True)
            continue

        i_id = rho_id_tag.index[0]
        i = index_id[i_id]
        pile = find_pile_member(id_index, distance[i], distance_c)
        # pile.sort(key=lambda v:rho_id[v],reverse=True)
        delta_id = delta_random_function(rho_id, delta_id, pile, i_id)
        pile, delta_id = pile_children(index_id, id_index, distance, distance_c, pile, rho_id, delta_id)
        # pile.sort(key=lambda v:rho_id[v],reverse=True)
        rho_set_tag(rho_id_tag, pile)
        next = 0
        # 假设当前是新类
        state = True
        outlier = False
        pile_id = pile_id.sort_values(by='size', ascending=False)
        if level is "DEBUG":
            save_show_cluster(index_id, data, distance_c, pile_id, dataset=dataset, level=level,
                              level_info="before find new cluster")
        # debug_show_cluster(index_id, data, distance_c, pile_id)
        # TODO
        # 合并得不好，合并的次数太少了，没有考虑合并后，可以继续合并的情况，参看debug2017-05-02-10-22-08信息
        while len(pile_id) > next:
            # 寻找下一个可能的堆的合并
            pre = pile_id.loc[next, 'pile']

            p1,cache = pile_children(index_id, id_index, distance, border, pile, rho_id, delta_id)
            p2,cache = pile_children(index_id, id_index, distance, border, pre, rho_id, delta_id)

            intersection = pile_intersection(p1, p2)
            # intersection = pile_intersection(pile, pre)
            if len(intersection) <= 0:
                # 不存在交集的情况
                next += 1
                continue
            elif len(intersection) > pile_max:
                # inter=pile_intersection(pile,pre)
                # if len(pile_brother(index_id, id_index, distance, distance_c, inter, pile_max)) < pile_max:
                # 存在交集，而且交集数量已经达到，聚类数
                # log.warning(pile_brother(index_id, id_index, distance, distance_c, intersection, pile_min, state=True))
                # log.fatal(str(len(pile_brother(index_id, id_index, distance, distance_c, intersection, pile_min, state=True)))+"\t"+str(len(intersection)))
                # if(len(pile_brother(index_id, id_index, distance, distance_c, intersection, pile_min, state=True))>len(intersection)):
                # pile = list(set(pile_sub(pile, intersection)))
                # next += 1
                # # 设置离群点
                # # if len(pile) <= 1:
                # if len(pile) <= pile_min:
                #     # 离群点的发现
                #     outlier = True
                #     break
                # continue
                state = False
                pile = list(set(pile_union(pile, pre)))
                # log.debug(pile_id)
                pile_id = pile_id.drop(next)
                # pile_id.ix[next, 'pile']=pile could not add list value to the pile_id
                # 进行重新排序
                pile_id = pile_id.reset_index(drop=True)
                next = 0
                # log.warn(rho_id)
                rho_set_tag(rho_id_tag, pile)
                # log.critical(rho_id)
                # next += 1



        if state == True:
            # 对data_id和pile_id表，进行处理标识
            # data_id.ix[i_id, 'pile'] = p_id
            # m = m + len(pile)
            rho_set_tag(rho_id_tag, pile)
            pile_id = pile_id.append(
                DataFrame([dict(pile=pile, p_id=p_id, size=len(pile), outlier=outlier)]),ignore_index=True)
        else:
            rho_set_tag(rho_id_tag, pile)
            pile_id = pile_id.append(
                DataFrame([dict(p_id=p_id, pile=pile, size=len(pile), outlier=False)]),ignore_index=True)

        pile_id = pile_id.reset_index(drop=True)
        pile_id = pile_id.sort_values('size', ascending=False)




        if level is "DEBUG":
            save_show_cluster(index_id, data, distance_c, pile_id, dataset=dataset, level=level,
                              level_info=str("after find new cluster:" + str(len(pile_id))))
        #     pile_id, delta_id = debug_pile_check(data, dataset, level, index_id, id_index, distance, distance_c, rho_id,
        #                                          delta_id, pile_id, pile_min)
        #     if len(pile_id)>3:
        #          exit()
        # else:
        #     pile_id, delta_id = pile_check(index_id, id_index, distance, distance_c, rho_id, delta_id, pile_id,
        #                                    pile_min)
        """
        if pile is None:
            pile_id.ix[p_id, 'size']=0
        else:
            pile_id.ix[p_id, 'size'] = len(pile)
        """

        k = pile_id['size'].sum()
        kk = (rho_id_tag > 0).sum()
        # log.debug("this is "+str(k)+" times, there has "+str(n-m)+" element has not clustering.")

    log.info("end computing pile, in distance_c:" + str(static_distance_c) + ". pile count about:" + str(
        pile_id.shape[0]) + " pile_max:" + str(pile_max) + " pile_min:" + str(pile_min))
    return pile_id


def ent_dc_step_by_step(id_index, index_id, data, threshold, distance, distance_c, dataset='none'):
    """
    :param id_index:
    :param index_id:
    :param data:
    :param threshold:
    :param distance:
    :param distance_c:
    :return:
    """
    # TODO modify the clustering without outlier
    i = 0
    level = "INFO"
    N = int(index_id.shape[0])
    # next_distance_c=get_next_distance_c(distance,distance_c)
    max_distance_c = max_distance(distance, distance_c)
    learning_rate = 0
    gradient = 0.00001
    jarge_now = 0
    jarge_pre = 5
    pre = 65535


    # 方差步长
    temp = distance.copy()
    # cache=temp.ravel()

    # percent = 0.2
    # position = int(index_id.shape[0] * (index_id.shape[0] + 1) / 2 * percent / 100)
    # log.debug("init the first max distance_c:" + str(max_distance_c) + " distance shape:" + str(distance.shape)+" start:"+str(sorted(cache)[position * 2 + index_id.shape[0]]))
    # distance_c = sorted(cache)[position * 2 + index_id.shape[0]]

    temp[np.isnan(temp)] = 0
    stand = np.std(temp)
    temp = distance.copy()

    temp[np.isnan(temp)] = stand

    temp = temp.min(axis=0)
    next_distance_c = np.std(temp)

    clusterRecorder = ClusterRecorder(dataset)
    cr_i = str(Properties.name_str_static() + "#" + str(i))

    # DataFrame([], columns=['id', 'start', 'end', 'd_c', 'max_distance_c', 'dataset', 'pile_size', 'H','note'])

    clusterRecorder.setValue(str(cr_i), 'id', Properties.name_str_static())
    clusterRecorder.setValue(str(cr_i), 'start', Properties.name_str_HMS())
    clusterRecorder.setValue(str(cr_i), 'd_c', distance_c)
    clusterRecorder.setValue(str(cr_i), 'max_distance_c', max_distance_c)
    clusterRecorder.setValue(str(cr_i), 'dataset', dataset)
    clusterRecorder.setValue(str(cr_i), 'pile_size', N)
    clusterRecorder.setValue(str(cr_i), 'H', 65535)
    clusterRecorder.setValue(str(cr_i), 'note', '整个算法运行时间')
    if learning_rate != 0:
        distance_c = distance_c + learning_rate

    start_time = Properties.name_str_HMS()

    while max_distance_c >= distance_c:
        i = i + 1
        last_time = Properties.name_str_HMS()
        # pile = 0
        # 设置pile的pile元素，与pile的类成员个数
        pile_id = DataFrame([], columns=['p_id', 'pile', 'size', 'outlier'])
        # delta_id, data_id = delta_function(id_index, index_id, rho_id, distance)
        # data = DataFrame([], columns=['gamma', 'rho', 'delta', 'pile'], index=index_id.index)
        data_id = DataFrame([], columns=['i_id', 'j_id', 'rho', 'delta', 'gamma', 'i', 'j', 'pile'],
                            index=id_index.values)
        pile_id = pile_function(pile_id, id_index, index_id, data, distance, distance_c, next_distance_c, dataset)
        pile_size = pile_id['size']
        pile = pile_id.shape[0] - np.sum(pile_id['outlier'])
        # id_index, index_id

        e=[]
        e_outlier=0
        #log.fatal(pile_size.values)


        pile_id = pile_id.sort_values('size', ascending=False)
        pile_id = pile_id.reset_index(drop=True)
        for i in range(0,len(pile_id)):
            if not pile_id.loc[i,'outlier']:
                e.append(pile_id.loc[i,'size'])
            else:
                e_outlier+=pile_id.loc[i,'size']
            if e_outlier>0:
                e.append(e_outlier)

        ee=np.array(e)
        e = _calc_ent(ee / N)
        merge = list([e, distance_c, pile])
        threshold = add_row(threshold, merge)
        jarge_now = pre - e
        # if jarge_now > jarge_pre:
        if jarge_now > 0:
            cr_j = str(Properties.name_str_static() + "#" + str(i))
            # DataFrame([], columns=['id', 'start', 'end', 'd_c', 'max_distanc', 'dataset', 'pile_size', 'H','note'])
            clusterRecorder.setValue(str(cr_j), 'id', Properties.name_str_static())
            clusterRecorder.setValue(str(cr_j), 'start', last_time)
            clusterRecorder.setValue(str(cr_j), 'd_c', distance_c)
            clusterRecorder.setValue(str(cr_j), 'max_distance_c', max_distance_c)
            clusterRecorder.setValue(str(cr_j), 'dataset', dataset)
            clusterRecorder.setValue(str(cr_j), 'pile_size', len(pile_id))
            clusterRecorder.setValue(str(cr_j), 'H', e)
            clusterRecorder.setValue(str(cr_j), 'note', '发现新下降时间')
            clusterRecorder.setValue(str(cr_j), 'end', Properties.name_str_HMS())

            save_show_cluster(index_id, data, distance_c, pile_id, dataset)

            cr_j = str(Properties.name_str_static() + "#" + str(i))
            # DataFrame([], columns=['id', 'start', 'end', 'd_c', 'max_distanc', 'dataset', 'pile_size', 'H','note'])
            clusterRecorder.setValue(str(cr_j), 'id', Properties.name_str_static())
            clusterRecorder.setValue(str(cr_j), 'start', start_time)
            clusterRecorder.setValue(str(cr_j), 'd_c', distance_c)
            clusterRecorder.setValue(str(cr_j), 'max_distance_c', max_distance_c)
            clusterRecorder.setValue(str(cr_j), 'dataset', dataset)
            clusterRecorder.setValue(str(cr_j), 'pile_size', len(pile_id))
            clusterRecorder.setValue(str(cr_j), 'H', e)
            clusterRecorder.setValue(str(cr_j), 'note', '发现新下降时间')
            clusterRecorder.setValue(str(cr_j), 'end', Properties.name_str_HMS())
            save_show_cluster(index_id, data, distance_c, pile_id, dataset)
            start_time = Properties.name_str_HMS()
            clusterRecorder.save()
            if level is "DEBUG":
                pile_id = pile_function(pile_id, id_index, index_id, data, distance, distance_c - next_distance_c,
                                        next_distance_c, dataset, level="DEBUG")
                save_show_cluster(index_id, data, distance_c, pile_id, dataset, level="DEBUG")



        pre = e
        # jarge_now = jarge_now + 1
        # jarge_pre = jarge_now
        # next_distance_c = get_next_distance_c(distance, distance_c)
        # next_distance_c = 0


        distance_c = distance_c + next_distance_c

        # if gradient==0.00005:
        #
        #     distance_c = distance_c + gradient
        #     gradient = gradient + 0.00001
        # elif learning_rate != 0:
        #     distance_c = distance_c + learning_rate
        #     gradient = 0.00001
        # else:
        #     distance_c = distance_c + next_distance_c
        #     gradient = 0.00001

        # distance_c = distance_c + learning_rate
        if e == 0:
            log.debug("e is 0.")
            break

        log.info(
            str(i) + " time, finished the next_distance_c about: " + str(next_distance_c) + " distance_c:" + str(
                distance_c) + " next-learning_rate:" + str(learning_rate) + " H:" + str(e))
    clusterRecorder.setValue(str(cr_i), 'end', Properties.name_str_HMS())
    clusterRecorder.save()
    log.debug(threshold)
    return threshold


def debug_cluster(id_index, index_id, data, distance, distance_c, next_distance_c, dataset='none',level="DEBUG"):
    i = 0
    N = int(index_id.shape[0])
    log.debug("init the distance_c:" + str(distance_c))
    # 设置pile的pile元素，与pile的类成员个数
    pile_id = DataFrame([], columns=['p_id', 'pile', 'size', 'outlier'])
    # delta_id, data_id = delta_function(id_index, index_id, rho_id, distance)
    # data = DataFrame([], columns=['gamma', 'rho', 'delta', 'pile'], index=index_id.index)
    pile_id = pile_function(pile_id, id_index, index_id, data, distance, distance_c, next_distance_c, dataset,
                            level=level)
    pile_size = pile_id['size']
    # pile = pile_id.shape[0] - np.sum(pile_id['outlier'])
    # id_index, index_id
    e = _calc_ent(pile_size.values / N)
    save_show_cluster(index_id, data, distance_c, pile_id, dataset)
    log.warn(" record the data status: " + str(distance.shape) + " distance_c:" + str(
        distance_c) + " threshold:" + str(e))

    return pile_id


def _calc_ent(probs):
    """
    计算信息熵
    :param probs: numpy结构
    :return: 返回probs的信息熵
    """
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


def save_show_cluster(index_id, data, distance_c, pile_id, dataset="/", level="INFO", level_info='scatter figure'):
    from view import plot_utils
    from context import resource_manager
    path = resource_manager.Properties.getDefaultDataFold() + "result" + resource_manager.getSeparator() + "temp/" + dataset + "/" + resource_manager.Properties.name_str_static() + "/"

    level_path = resource_manager.Properties.getDefaultDataFold() + "result" + resource_manager.getSeparator() + "temp/" + level + "/" + resource_manager.Properties.name_str_static() + "/" + str(
        distance_c) + "/"

    if not os.path.exists(path[:path.rfind('/')]):
        os.makedirs(path[:path.rfind('/')])
    if not os.path.exists(level_path[:level_path.rfind('/')]):
        os.makedirs(level_path[:level_path.rfind('/')])

    pile_id = pile_id.sort_values('size', ascending=False)
    x = []
    y = []
    label = []
    i = 1
    for m in range(len(pile_id)):
        # l=pile_id.irow(m)['pile']
        l = pile_id.iloc[m]['pile']
        # size=pile_id.irow(m)['size']
        size = pile_id.iloc[m]['size']

        if pile_id.loc[m]['outlier'] is False:
            for node in l:
                index = index_id[node]
                x.append(data[index][0])
                y.append(data[index][1])
                label.append(i)
            i = i + 1
        else:
            for node in l:
                index = index_id[node]
                x.append(data[index][0])
                y.append(data[index][1])
                label.append(0)
    if level is "SEE":
        plot_utils.plot_scatter_diagram(None, x=x, y=y, x_label='x', y_label='y', title=level_info, label=label)
    if level is "DEBUG":
        # plot_utils.save_scatter_diagram(None, x=x, y=y, x_label='x', y_label='y', title='scatter figure', label=label,path=level_path+resource_manager.Properties.name_str_FULL()+".png")

        plot_utils.save_all_scatter_diagram(None, x=x, y=y, x_label='x', y_label='y', title=level_info, label=label,
                                            path=level_path + resource_manager.Properties.name_str_FULL() + ".png")
    else:
        plot_utils.save_scatter_diagram(None, x=x, y=y, x_label='x', y_label='y', title='scatter figure', label=label,
                                        path=path + str(
                                            distance_c) + ".png")
        plot_utils.save_all_scatter_diagram(None, x=x, y=y, x_label='x', y_label='y', title='scatter figure',
                                            label=label,
                                            path=path + str(
                                                distance_c) + ".png")

    # plot_utils.plot_scatter_diagram(None, x=x, y=y, x_label='x', y_label='y', title='scatter figure', label=label)
    log.debug(("\n") + str(pile_id))
    try:
        p = Properties.getDefaultDataFold() + "/csv/" + dataset + "/" + resource_manager.Properties.name_str_static() + "/" + str(
            distance_c) + ".csv"
        pile_id.to_csv(p)
    except:
        if not os.path.exists(p[:p.rfind('/')]):
            pp = p.rfind('/')
            os.makedirs(p[:pp])
        os.mknod(p)
        pile_id.to_csv(p)


# def show_cluster(index_id, data, distance_c, pile_id):
#     from view import plot_utils
#     pile_id = pile_id.sort_values('size', ascending=False)
#     x = []
#     y = []
#     label = []
#     i = 1
#     for m in range(len(pile_id)):
#         # l=pile_id.irow(m)['pile']
#         l = pile_id.iloc[m]['pile']
#         # size=pile_id.irow(m)['size']
#         size = pile_id.iloc[m]['size']
#         if size > 1:
#             for node in l:
#                 index = index_id[node]
#                 x.append(data[index][0])
#                 y.append(data[index][1])
#                 label.append(i)
#             i = i + 1
#         else:
#             for node in l:
#                 index = index_id[node]
#                 x.append(data[index][0])
#                 y.append(data[index][1])
#                 label.append(0)
#
#     plot_utils.plot_scatter_diagram(None, x=x, y=y, x_label='x', y_label='y', title='scatter figure', label=label)
#
#     log.debug(label)


def binary_array(data):
    # data wuold be modify

    data[data > 200] = 0
    data[data > 0] = 1
    # log.debug(data)
    return data


def cluster(id, data, dataset):
    from pandas import Series, DataFrame
    id_index = Series(id.tolist())
    from cluster import density_cluster
    N = id_index.count()
    distance = compute_distance(data)
    distance_c = min_distance(distance)
    # id.values -> 对应的key
    index_id = Series(id_index.index, index=id_index.values)
    log.warn("the init distance_c is: " + str(distance_c))
    # to creat the base index table
    # 生成对应的索引，用于控制rho，delta，index的内容
    rho_id = rho_function(index_id, distance, distance_c=distance_c)
    # delta_id, data_id = delta_function(id_index, index_id, rho_id, distance)
    # gamma=rho*delta
    threshold = DataFrame([], columns=['H', 'd_c', 'cluster'])
    threshold = ent_dc_step_by_step(id_index, index_id, data, threshold=threshold, distance=distance,
                                    distance_c=distance_c, dataset=dataset)
    r = threshold
    # log.debug("rho:\n" + str(rho))
    log.debug("threshold\n" + str(DataFrame(threshold)))
    return r


class ClusterRecorder:
    """
    设置记录类
    :return:
    """

    def __init__(self, dataset):
        self.dataset = dataset
        try:
            self.recorder_csv = pandas.read_csv(
                Properties.getDefaultDataFold() + "/csv/recorder_csv_" + self.dataset + ".csv", index_col=0)
        except:
            self.recorder_csv = DataFrame([], columns=['id', 'start', 'end', 'd_c', 'max_distance_c', 'dataset',
                                                       'pile_size', 'H', 'note'])

    def setValue(self, row, columns, value):
        self.recorder_csv.set_value(row, columns, value)
        self.recorder_csv.set_value(row, 'end', Properties.name_str_FULL())

    def save(self):
        self.recorder_csv.to_csv(Properties.getDefaultDataFold() + "/csv/recorder_csv_" + self.dataset + ".csv")


class Queue:
    """模拟队列"""

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
