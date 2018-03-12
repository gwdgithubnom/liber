#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from tools import logger
import numpy as np
from sklearn import manifold
from sklearn import __version__ as sklearn_version
from view import plot_utils
from  view import  plot
from cluster import cluster_dpc
from context import  resource_manager


log = logger.getLogger()
from cluster import *


def run(data, auto_select_dc=False,filetype="txt"):
    dpcluster = cluster_dpc.DensityPeakCluster()
    distances, max_dis, min_dis, max_id, rho = dpcluster.local_density(cluster_dpc.load_paperdata, data,
                                                                       auto_select_dc=auto_select_dc,filetype=filetype)
    delta, nneigh = cluster_dpc.min_distance(max_id, max_dis, distances, rho)
    plot.plot_rho_delta(rho, delta)  # plot to choose the threthold


if __name__ == '__main__':
    # plot('./data/data_in_paper/example_distances.dat')
    #run(resource_manager.Properties.getDefaultDataFold()+'xml/iris.xml', auto_select_dc=True,filetype="xml")
    #run(resource_manager.Properties.getDefaultDataFold()+'txt/iris.data.tmp.txt', auto_select_dc=True)
    run(resource_manager.Properties.getDefaultDataFold()+'xml/flame.xml', auto_select_dc=True,filetype="xml")