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
from cluster.density_cluster import *
from cluster import density_cluster

def multi_ent_dc_step_by_step(id_index, index_id, threshold, distance, distance_c, max_distance_c):
    i = 0
    learning_rate = 0.5
    N = int(index_id.shape[0])
    # next_distance_c=get_next_distance_c(distance,distance_c)
    # max_distance_c = max_distance(distance, distance_c)
    distance_c = distance_c
    log.debug("init the first max distance_c:" + str(max_distance_c))
    while max_distance_c >= distance_c:
        i = i + 1
        pile = 0
        # 设置pile的pile元素，与pile的类成员个数
        pile_id = DataFrame([], columns=['pile', 'size', 'outlier'])
        # delta_id, data_id = delta_function(id_index, index_id, rho_id, distance)
        # data = DataFrame([], columns=['gamma', 'rho', 'delta', 'pile'], index=index_id.index)
        data_id = DataFrame([], columns=['j_id', 'rho', 'delta', 'gamma', 'i', 'j', 'pile'], index=id_index.values)
        pile_id = pile_function(pile_id, id_index, index_id, data_id, distance, distance_c)
        pile_size = pile_id['size']
        pile = np.sum(pile_id['outlier'])
        # id_index, index_id
        e = density_cluster._calc_ent(pile_size.values / N)
        merge = list([e, distance_c, pile])
        threshold = add_row(threshold, merge)
        # distance_c = distance_c + next_distance_c +1
        next_distance_c = get_next_distance_c(distance, distance_c)

        distance_c = distance_c + next_distance_c
        log.info(str(i) + " time, finished the data about: " + str(distance.shape) + " distance_c:" + str(
            distance_c) + " next learning_rate:" + str(learning_rate))
    return threshold


def multi_processing_cluster(job, work, df, id, data):
    # threshold = DataFrame([], columns=['H', 'd_c', 'cluster'])
    from pandas import Series, DataFrame
    id_index = Series(id.tolist())
    from cluster import density_cluster
    N = id_index.count()
    distance = compute_distance(data)
    distance_c = min_distance(distance)
    max = max_distance(distance, distance_c)
    max = average_task(max, job)
    log.debug(str("max:") + str(max))
    distance_c = distance_c + work * max
    max_distance_c = distance_c + max
    # id.values -> 对应的key
    index_id = Series(id_index.index, index=id_index.values)
    log.warn("work id " + str(work) + " the starting distance_c is: " + str(distance_c) + ". working under" + str(
        max_distance_c))
    # to creat the base index table
    # 生成对应的索引，用于控制rho，delta，index的内容
    rho_id = rho_function(index_id, distance, distance_c=distance_c)
    delta_id, data_id = delta_function(id_index, index_id, rho_id, distance)
    # gamma=rho*delta
    threshold = df
    threshold = multi_ent_dc_step_by_step(id_index, index_id, threshold=threshold, distance=distance,
                                          distance_c=distance_c, max_distance_c=max_distance_c)
    r = threshold
    # log.debug("rho:\n" + str(rho))
    log.debug("worker " + str(work) + " has finished. threshold\n" + str(DataFrame(threshold)))






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

def average_task(max, piece):
    distance = max / piece
    return math.floor(distance)
