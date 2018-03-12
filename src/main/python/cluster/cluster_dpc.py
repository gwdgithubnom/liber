#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import math
from tools import logger
import numpy as np
import os
log = logger.getLogger()

def conv(o):
    x = np.array(o)
    y = x.astype(np.float)
    return y


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
    sum_p=np.sum(point_k)
    return np.sqrt(sum_p)

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

def load_paperdata(distance_f,filetype="txt"):
    '''
    Load distance from data

    Args:
            distance_f : distance file, the format is column1-index 1, column2-index 2, column3-distance

    Returns:
        distances dict, max distance, min distance, max continues id
    '''
    if filetype=="xml":
        from context.resource_manager import Properties
        from pandas import DataFrame, Series
        path = os.path.join(distance_f)
        from xml.dom.minidom import parse, parseString
        datas = parse(path)
        id = []
        data = []
        for node in datas.getElementsByTagName("Image"):
            idNode = node.getElementsByTagName("id")[0].childNodes[0].data
            id.append(idNode)
            dataNode = node.getElementsByTagName("data")[0].childNodes[0].data
            dataNode = dataNode[1:-1].split(',')
            data.append(dataNode)
        id = np.asarray(id)
        id = Series(id)
        data = np.asarray(list(map(conv, data)), dtype=np.float)
        id_index = Series(id.tolist())
        from cluster import density_cluster
        N = id_index.count()
        index_id = Series(id_index.index, index=id_index.values)
        distance=compute_distance(data)
        distances={}
        for i in range(0,N):
            for j in range(i+1,N):
                distances[(i, j)] = (distance[i][j])
                distances[(j,i)] = (distance[i][j])
            #distances[(i,i)]=0
        max_id=N-1
        for i in range(max_id):
            distances[(i, i)] = 0.0
        # max_dis=float(distance)
        min_dis=min(distances.items(),key=lambda x: x[1])[1]
        max_dis=max(distances.items(),key=lambda x: x[1])[1]
        print(len(distances))
        #print(distances)
        #print(min_dis)
        #print(max_dis)
        # print(min_dis)
        # print(distances[min(distances)])
        # print(distances[max(distances)])
        # print(max_dis)
        return distances, max_dis, min_dis, max_id
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
    log.info("PROGRESS: load end")
    # print(min_dis)
    # print(max_dis)
    # print(max_id)
    # print(distances)
    # print(distances[min_dis])
    # print(distances[max_dis])
    print(len(distances))
    return distances, max_dis, min_dis, max_id


def select_dc(max_id, max_dis, min_dis, distances, auto=False):
    '''
    Select the local density threshold, default is the method used in paper, auto is `autoselect_dc`

    Args:
            max_id    : max continues id
            max_dis   : max distance for all points
            min_dis   : min distance for all points
            distances : distance dict
            auto      : use auto dc select or not

    Returns:
        dc that local density threshold
    '''
    log.info("PROGRESS: select dc")
    if auto:
        return autoselect_dc(max_id, max_dis, min_dis, distances)
    percent = 2.0
    position = int(max_id * (max_id + 1) / 2 * percent / 100)
    dc = sorted(distances.values())[position * 2 + max_id]
    log.info("PROGRESS: dc - " + str(dc))
    return dc


def autoselect_dc(max_id, max_dis, min_dis, distances):
    '''
    Auto select the local density threshold that let average neighbor is 1-2 percent of all nodes.

    Args:
            max_id    : max continues id
            max_dis   : max distance for all points
            min_dis   : min distance for all points
            distances : distance dict

    Returns:
        dc that local density threshold
    '''
    dc = (max_dis + min_dis) / 2

    while True:
        nneighs = sum([1 for v in distances.values() if v < dc]) / max_id ** 2
        if nneighs >= 0.01 and nneighs <= 0.02:
            break
        # binary search
        if nneighs < 0.01:
            min_dis = dc
        else:
            max_dis = dc
        dc = (max_dis + min_dis) / 2
        if max_dis - min_dis < 0.0001:
            break
    return dc


def local_density(max_id, distances, dc, guass=True, cutoff=False):
    '''
    Compute all points' local density

    Args:
            max_id    : max continues id
            distances : distance dict
            gauss     : use guass func or not(can't use together with cutoff)
            cutoff    : use cutoff func or not(can't use together with guass)

    Returns:
        local density vector that index is the point index that start from 1
    '''
    assert guass ^ cutoff
    log.info("PROGRESS: compute local density")
    guass_func = lambda dij, dc: math.exp(- (dij / dc) ** 2)
    cutoff_func = lambda dij, dc: 1 if dij < dc else 0
    func = guass and guass_func or cutoff_func
    rho = [-1] + [0] * max_id
    for i in range(1, max_id):
        for j in range(i + 1, max_id + 1):
            rho[i] += func(distances[(i, j)], dc)
            rho[j] += func(distances[(i, j)], dc)
        if i % (max_id / 10) == 0:
            log.info("PROGRESS: at index #%i" % (i))
    return np.array(rho, np.float32)


def min_distance(max_id, max_dis, distances, rho):
    '''
    Compute all points' min distance to the higher local density point(which is the nearest neighbor)

    Args:
            max_id    : max continues id
            max_dis   : max distance for all points
            distances : distance dict
            rho       : local density vector that index is the point index that start from 1

    Returns:
        min_distance vector, nearest neighbor vector
    '''
    log.info("PROGRESS: compute min distance to nearest higher density neigh")
    sort_rho_idx = np.argsort(-rho)
    delta, nneigh = [0.0] + [float(max_dis)] * (len(rho) - 1), [0] * len(rho)
    delta[sort_rho_idx[0]] = -1.
    for i in range(1, max_id):
        for j in range(0, i):
            old_i, old_j = sort_rho_idx[i], sort_rho_idx[j]
            if distances[(old_i, old_j)] < delta[old_i]:
                delta[old_i] = distances[(old_i, old_j)]
                nneigh[old_i] = old_j
        if i % (max_id / 10) == 0:
            log.info("PROGRESS: at index #%i" % (i))
    delta[sort_rho_idx[0]] = max(delta)
    return np.array(delta, np.float32), np.array(nneigh, np.float32)


class DensityPeakCluster(object):

    def local_density(self, load_func, distance_f, dc=None, auto_select_dc=False,filetype="txt"):
        '''
        Just compute local density

        Args:
            load_func     : load func to load data
            distance_f    : distance data file
            dc            : local density threshold, call select_dc if dc is None
            autoselect_dc : auto select dc or not

        Returns:
            distances dict, max distance, min distance, max index, local density vector
        '''
        assert not (dc is not None and auto_select_dc)
        distances, max_dis, min_dis, max_id = load_func(distance_f,filetype)
        if dc is None:
            dc = select_dc(max_id, max_dis, min_dis,
                           distances, auto=auto_select_dc)
        rho = local_density(max_id, distances, dc)
        return distances, max_dis, min_dis, max_id, rho

    def cluster(self, load_func, distance_f, density_threshold, distance_threshold, dc=None, auto_select_dc=False,filetype="txt"):
        '''
        Cluster the data

        Args:
            load_func          : load func to load data
            distance_f         : distance data file
            dc                 : local density threshold, call select_dc if dc is None
            density_threshold  : local density threshold for choosing cluster center
            distance_threshold : min distance threshold for choosing cluster center
            autoselect_dc      : auto select dc or not

        Returns:
            local density vector, min_distance vector, nearest neighbor vector
        '''
        assert not (dc is not None and auto_select_dc)
        distances, max_dis, min_dis, max_id, rho = self.local_density(
            load_func, distance_f, dc=dc, auto_select_dc=auto_select_dc,filetype=filetype)
        delta, nneigh = min_distance(max_id, max_dis, distances, rho)
        log.info("PROGRESS: start cluster")
        cluster, ccenter = {}, {}  # cl/icl in cluster_dp.m
        for idx, (ldensity, mdistance, nneigh_item) in enumerate(zip(rho, delta, nneigh)):
            if idx == 0:
                continue
            if ldensity >= density_threshold and mdistance >= distance_threshold:
                ccenter[idx] = idx
                cluster[idx] = idx
        for idx, (ldensity, mdistance, nneigh_item) in enumerate(zip(rho, delta, nneigh)):
            if idx == 0 or idx in ccenter:
                continue
            if nneigh_item in cluster:
                cluster[idx] = cluster[nneigh_item]
            else:
                cluster[idx] = -1
            if idx % (max_id / 10) == 0:
                log.info("PROGRESS: at index #%i" % (idx))
        self.cluster, self.ccenter = cluster, ccenter
        self.distances = distances
        self.max_id = max_id
        log.info("PROGRESS: ended")
        return rho, delta, nneigh
