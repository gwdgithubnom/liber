#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import math
import logging
import numpy as np
from PIL import Image
#from PIL.Image import core as image
import os, random, string, shutil
from context.resource_manager import Properties

logger = logging.getLogger("dpc_cluster")

def compute_point_distance(point_i,point_j):
    point_k=(point_i-point_j)*(point_i-point_j)
    return np.sum(point_k)

def compute_distance_from_xml(path=Properties.getImageXmlResource()):
    from xml.dom.minidom import parse,parseString
    images=parse(path)
    for node in images.getElementById("Image"):




