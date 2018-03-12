#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from tools import logger
import numpy as np
from sklearn import manifold
from sklearn import __version__ as sklearn_version
from view import plot_utils
from  view import  plot
from cluster import cluster_dpc

from view.plot_utils import *
from cluster.cluster_dpc import *
from context import  resource_manager
log = logger.getLogger()
from cluster import *


def run(data, density_threshold, distance_threshold, auto_select_dc=False,filetype="txt"):

    dpcluster = DensityPeakCluster()
    rho, delta, nneigh = dpcluster.cluster(cluster_dpc.load_paperdata, data, density_threshold, distance_threshold,
                                           auto_select_dc=auto_select_dc,filetype=filetype)
    log.info(str(len(dpcluster.ccenter)) + ' center as below')
    for idx, center in dpcluster.ccenter.items():
        log.info('%d %f %f' % (idx, rho[center], delta[center]))
    # plot_rho_delta(rho, delta)   #plot to choose the threthold
    plot.plot_cluster(dpcluster)


if __name__ == '__main__':
    # plot('./data/data_in_paper/example_distances.dat', 20, 0.1)
    #run(resource_manager.Properties.getDefaultDataFold()+'txt/iris.data.tmp.txt', 4, 1.3, auto_select_dc=True)
    #run(resource_manager.Properties.getDefaultDataFold()+'xml/iris.xml', 4, 1.3, auto_select_dc=True,filetype="xml")
    run(resource_manager.Properties.getDefaultDataFold()+'xml/flame.xml', 2, 2, auto_select_dc=True,filetype="xml")
    #run(resource_manager.Properties.getDefaultDataFold()+'xml/iris.xml', auto_select_dc=True,filetype="xml")