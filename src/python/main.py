from numpy import *
from pandas import *
from tools import logger

log=logger.getLogger()

if __name__ == '__main__':
    from context.resource_manager import Properties
    from cluster import density_cluster
    id=np.load(Properties.getRootPath()+"/data/cache/id.npy")
    data=np.load(Properties.getRootPath()+"/data/cache/data.npy")
    density_cluster.cluster(id,data)

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




