import sys,getopt
from context import resource_manager
import math
from pandas import DataFrame
from context.resource_manager import Properties
from cluster import density_cluster
import os

def save_dataframe_csv(threshold=DataFrame(),name="default",relative=True):
    if not os.path.exists(Properties.getDefaultDataFold()+"/csv/"+name+"/"+resource_manager.Properties.name_str_static()):
        #f=open(Properties.getDefaultDataFold()+"/csv/threshold.csv","w")
        #f.close()
        os.makedirs(Properties.getDefaultDataFold()+"/csv/"+name+"/"+resource_manager.Properties.name_str_static())
    threshold.to_csv(Properties.getDefaultDataFold()+"/csv/"+name+"/"+resource_manager.Properties.name_str_static()+"/threshold.csv")