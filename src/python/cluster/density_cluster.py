#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import math
import logging
import numpy as np
from PIL import Image
#from PIL.Image import core as image
import os, random, string, shutil

logger = logging.getLogger("dpc_cluster")

def compute_point_distance(point_i,point_j):
    point_k=point_i*point_j+point_i*point_j
    return point_k