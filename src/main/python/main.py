from numpy import *
from pandas import *
from tools import logger
import  shutil
import os
import sys,getopt
from context import resource_manager
import math

log = logger.getLogger()

def conv(o):
    x = np.array(o)
    y = x.astype(np.float)
    return y

def save(name='default'):
    """
    保存id和data数据
    :return:
    """
    from context.resource_manager import Properties
    from pandas import DataFrame, Series
    path = os.path.join(Properties.getXmlLocation()+name+".xml")
    from xml.dom.minidom import parse, parseString
    images = parse(path)
    id = []
    data = []
    for node in images.getElementsByTagName("Image"):
        idNode = node.getElementsByTagName("id")[0].childNodes[0].data
        id.append(idNode)
        dataNode = node.getElementsByTagName("data")[0].childNodes[0].data
        dataNode = dataNode[1:-1].split(',')
        data.append(dataNode)
    id = np.asarray(id)
    id = Series(id)
    data = np.asarray(list(map(conv, data)), dtype=np.float)
    if not os.path.exists(Properties.getDefaultDataFold()+"/cache/"+name):
        #f=open(Properties.getDefaultDataFold()+"/csv/threshold.csv","w")
        #f.close()
        os.makedirs(Properties.getDefaultDataFold()+"/cache/"+name)
    np.save(Properties.getRootPath() + "/data/cache/"+name+"/id.npy", id)
    np.save(Properties.getRootPath() + "/data/cache/"+name+"/data.npy", data)
    # encoding='ascii'



def get_threshold(name='default'):
    """
    计算信息熵
    :return:
    """
    from context.resource_manager import Properties
    from view import shape_view
    from view import plot_utils
    from cluster import density_cluster
    id = np.load(Properties.getRootPath() + "/data/cache/"+name+"/id.npy")
    data = np.load(Properties.getRootPath() + "/data/cache/"+name+"/data.npy")
    #image_size= round(math.sqrt(float(data[0].shape[0])))
    #plot_utils.plot_image( data[551], w, w)
    # data=density_cluster.binary_array(data)
    # shape_view.pandas_view_record((data))
    threshold=density_cluster.cluster(id,data,dataset=name)
    if not os.path.exists(Properties.getDefaultDataFold()+"/csv/"+name):
        #f=open(Properties.getDefaultDataFold()+"/csv/threshold.csv","w")
        #f.close()
        os.makedirs(Properties.getDefaultDataFold()+"/csv/"+name)
    threshold.to_csv(Properties.getDefaultDataFold()+"/csv/"+name+"/threshold.csv")



def experiment(name="path"):
    try:
        opts,args=getopt.getopt(sys.argv[1:], "f:")
        name=opts[0][1]
        log.warn("using value:"+str(name))
    except:
        log.warn("using defualt value:"+str(name))
    log.warn(resource_manager.Properties.name_str_static())
    save(name=name)
    get_threshold(name=name)



def record_expriment(name='path'):
    from context.resource_manager import Properties
    from context import resource_manager
    from view import shape_view

    from cluster import density_cluster
    if os.path.exists(resource_manager.Properties.getDefaultDataFold()+"result/temp"+resource_manager.Properties.name_str_static() + resource_manager.getSeparator()):
        shutil.rmtree(resource_manager.Properties.getDefaultDataFold()+"result/temp"+resource_manager.Properties.name_str_static() + resource_manager.getSeparator())
    threshold=pandas.read_csv(Properties.getDefaultDataFold()+"/csv/"+name+"/"+resource_manager.Properties.name_str_static()+"/threshold.csv")
    save_plot(threshold)
    d_c=np.asarray(threshold['d_c'].values)
    path = resource_manager.Properties.getDefaultDataFold() + resource_manager.getSeparator() + "result" + resource_manager.getSeparator() + name+"/"+resource_manager.Properties.name_str_static()
    log.debug(threshold['cluster'].sort_values(ascending=False))
    shutil.copytree(resource_manager.Properties.getDefaultDataFold()+"result/temp"+resource_manager.getSeparator()+resource_manager.Properties.name_str_static() + resource_manager.getSeparator(),path)
    shutil.copy(Properties.getDefaultDataFold()+"/csv/"+name+"/"+resource_manager.Properties.name_str_static()+"/threshold.csv", path)
    log.warn("finished")


def save_plot(threshold):
    from view import plot_utils
    path=resource_manager.Properties.getDefaultDataFold()+resource_manager.getSeparator()+"result/temp"+resource_manager.getSeparator()+resource_manager.Properties.name_str_static() + resource_manager.getSeparator()+"threshold.png"
    plot_utils.save_scatter_diagram(None,x=threshold['d_c'].values,y=threshold['H'].values,x_label='delta',y_label='H',title='threshold scatter figure',path=path)
    plot_utils.plot_scatter_diagram(None,x=threshold['d_c'].values,y=threshold['H'].values,x_label='delta',y_label='H',title='threshold scatter figure')
    plot_utils.plot_scatter_diagram(None, x=threshold['H'].values, y=threshold['d_c'].values, x_label='delta',
                                    y_label='H', title='threshold scatter figure')
    plot_utils.save_scatter_diagram(None,x=threshold['d_c'].values,y=threshold['H'].values,x_label='delta',y_label='H',title='threshold scatter figure',path=path)

if __name__ == '__main__':
    experiment('path')













    """
    delta_index=Series(id,index=id,dtype=np.float)

    i=0
    order_id=Series(result[:,0],index=id_index.values)
    # to find the rho_j>rho_i
    order_id=order_id.sort_values()
    j=order_id.index[1]
    # to find the
    j=int(index_id[j])
    # to find the i'key
    k=str(id_index[i])

    delta_index[k]=int(result[i][j])
    print(delta_index)

    """
    # 构建delta的内容
