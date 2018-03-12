from tools import  image_xml_builder
from tools import logger
log=logger.getLogger()
from tools import  binaryzation_crop
from tools import  file_manage
from  tools import  image_xml_builder
from tools import  image_rebuild
from pandas import  DataFrame
import numpy as np
import pandas
from context import resource_manager
from context.resource_manager import  Properties

def load_data():
    id = np.load(Properties.getRootPath() + "/data/cache/flame/id.npy")
    data = np.load(Properties.getRootPath() + "/data/cache/flame/data.npy")

    return id,data

if __name__ == '__main__':
    id,data=load_data()
    label=[ int(x[0:1]) for x in id ]
    from context.resource_manager import Properties
    from view import shape_view
    from view import plot_utils
    from cluster import density_cluster
    x=data[:,:1]
    y=data[:,1:2]
    path=resource_manager.Properties.getDefaultDataFold()+resource_manager.getSeparator()+"result"+resource_manager.getSeparator()+"srv.png"
    plot_utils.save_scatter_diagram(None,x=x,y=y,x_label='x',y_label='y',title='scatter figure',label=label,path=path)
    #plot_utils.plot_scatter_diagram(None,x=x,y=y,x_label='x',y_label='y',title='scatter figure',label=label)
