from numpy import *
from pandas import *
from tools import logger
import os
import math

log = logger.getLogger()

def conv(o):
    x = np.array(o)
    y = x.astype(np.float)
    return y

def save():
    from context.resource_manager import Properties
    from pandas import DataFrame, Series
    path = os.path.join(Properties.getRootPath(), Properties.getImageXmlResource())
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
    if not os.path.exists(Properties.getDefaultDataFold()+"/cache/image7"):
        #f=open(Properties.getDefaultDataFold()+"/csv/threshold.csv","w")
        #f.close()
        os.makedirs(Properties.getDefaultDataFold()+"/cache/image7")
    np.save(Properties.getRootPath() + "/data/cache/image7/id.npy", id)
    np.save(Properties.getRootPath() + "/data/cache/image7/data.npy", data)


def get_threshold():
    from context.resource_manager import Properties
    from view import shape_view
    from view import plot_utils
    from cluster import density_cluster
    id = np.load(Properties.getRootPath() + "/data/cache/image7/id.npy")
    data = np.load(Properties.getRootPath() + "/data/cache/image7/data.npy")
    image_size= round(math.sqrt(float(data[0].shape[0])))
    #plot_utils.plot_image( data[551], w, w)
    data=density_cluster.binary_array(data)
    # shape_view.pandas_view_record((data))
    threshold=density_cluster.cluster(id,data)
    if not os.path.exists(Properties.getDefaultDataFold()+"/csv"):
        #f=open(Properties.getDefaultDataFold()+"/csv/threshold.csv","w")
        #f.close()
        os.makedirs(Properties.getDefaultDataFold()+"/csv")
    threshold.to_csv(Properties.getDefaultDataFold()+"/csv/threshold.csv")


if __name__ == '__main__':

    get_threshold()
    from context.resource_manager import Properties
    from view import shape_view
    from view import plot_utils
    from cluster import density_cluster
    threshold=pandas.read_csv(Properties.getDefaultDataFold()+"/csv/threshold.csv")
    d_c=np.asarray(threshold['d_c'].values)

    log.debug(threshold['cluster'].sort_values(ascending=False))
    plot_utils.plot_scatter_diagram(None,x=threshold['d_c'].values,y=threshold['H'].values,x_label='delta',y_label='H',title='threshold scatter figure')







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
