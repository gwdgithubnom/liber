from numpy import *
from pandas import *
from tools import logger
import os
import math

log = logger.getLogger()


def get_threshold():
    from context.resource_manager import Properties
    from view import shape_view
    from view import plot_utils
    from cluster import density_cluster
    id = np.load(Properties.getRootPath() + "/data/cache/id.npy")
    data = np.load(Properties.getRootPath() + "/data/cache/data.npy")
    image_size= round(math.sqrt(float(data[0].shape[0])))
    #plot_utils.plot_image( data[551], w, w)
    data=density_cluster.binary_array(data)
    # shape_view.pandas_view_record((data))
    import numpy
    import multiprocessing
    threshold = DataFrame([], columns=['H', 'd_c', 'cluster'])
    N=20
    pool = multiprocessing.Pool(processes=N)
    result = list(range(N))
    for i in range(N):
        pool.apply_async(density_cluster.cluster, (N,i,threshold,id,data))
        # d = numpy.concatenate([c, c], axis=0)
    pool.close()
    pool.join()
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
    log.debug(d_c)
    log.critical(type(d_c))
    plot_utils.plot_scatter_diagram(None,x=d_c,y=threshold['H'].values,x_label='delta',y_label='H',title='threshold scatter figure')







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
