from numpy import *
from pandas import *
from tools import logger

log=logger.getLogger()

if __name__ == '__main__':
    from context.resource_manager import Properties
    id=np.load(Properties.getRootPath()+"/data/cache/id.npy")
    data=np.load(Properties.getRootPath()+"/data/cache/data.npy")
    from pandas import Series,DataFrame

    id_index=Series(id.tolist())
    #d=DataFrame(data)
    from cluster import density_cluster
    result=density_cluster.compute_distance(data)
    rho=density_cluster.rho_function(result,distance_c=15039282)
    # to creat the base index table
    df=DataFrame(result)

    # 生成对应的索引，用于控制rho，delta，index的内容
    # id.values -> 对应的key
    rho_id=Series(rho,index=id)
    rho_id=rho_id.sort_values()
    index_id=Series(id_index.index,index=id_index.values)
    delta_index=density_cluster.delta_function(id_index,index_id,rho_id,result)

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




