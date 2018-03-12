from pandas import *
from pandas import DataFrame as df
import numpy
from tools import logger
from IPython.display import display

def pandas_view_record(object):
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.width', None)
    pandas.set_option('display.max_rows', None)
    from tools import logger
    logger.get_record_logger().debug(object)


def pandas_view_debug(object,width=1000):
    #pandas.set_option('expand_frame_repr', False)
    #None
    if width!=500:
        pandas.set_option('display.width', width)
    else:
        pandas.set_option('display.width', None)
    logger.getLogger().debug(object)


def pandas_view_info(object,width=1000):
    if width!=500:
        pandas.set_option('display.width', width)
    else:
        pandas.set_option('display.width', None)
    logger.getLogger().info(object)


def numpy_view(object,state="debug",width=500):
    if state=="info":
        pandas_view_info(DataFrame(object),width=width)
    elif state=="record":
        pandas_view_record(DataFrame(object))
    else:
        pandas_view_debug(DataFrame(object),width=width)
