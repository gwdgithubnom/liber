from numpy import *
from pandas import *
from tools import logger
import  shutil
import os
import sys,getopt
from context import resource_manager
from context import data_reader
from context import data_writer
from cluster import density_cluster
import math

log = logger.getLogger()

def experiment(name="path"):
    try:
        opts,args=getopt.getopt(sys.argv[1:], "f:")
        name=opts[0][1]
        log.warn("using value:"+str(name))
    except:
        log.warn("using defualt value:"+str(name))
    save_name=resource_manager.Properties.name_str_static()
    log.warn(resource_manager.Properties.name_str_static())
    id,data=data_reader.get_xml_data(name)
    threshold=density_cluster.cluster(id,data,name)
    data_writer.save_dataframe_csv(threshold,name)
    record_expriment(name,save_name)


def record_expriment(name='path',save_name='default'):
    from context.resource_manager import Properties
    from context import resource_manager
    from view import shape_view
    record_img_path=resource_manager.Properties.getDefaultDataFold()+"result/temp/"+name+"/"+save_name +"/"
    record_csv_path=Properties.getDefaultDataFold()+"/csv/"+name+"/"+save_name+"/"
    path = resource_manager.Properties.getDefaultDataFold() + "/result/" + name+"/"+save_name

    if not os.path.exists(record_csv_path):
        # shutil.rmtree(resource_manager.Properties.getDefaultDataFold()+"result/temp/"+save_name+ "/")
        os.makedirs(record_csv_path)
    threshold=pandas.read_csv(record_csv_path+"threshold.csv")

    save_plot(name,threshold,save_name)

    log.debug(threshold['cluster'].sort_values(ascending=False))
    shutil.copytree(record_img_path,path)
    shutil.copy(record_csv_path+"threshold.csv", path)
    log.warn("finished")


def save_plot(name,threshold,save_name='default',level="INFO"):
    from view import plot_utils
    path=resource_manager.Properties.getDefaultDataFold()+"result/temp/"+name+"/"+save_name +"/""threshold.png"

    plot_utils.save_scatter_diagram(None,x=threshold['d_c'].values,y=threshold['H'].values,x_label='delta',y_label='H',title='threshold scatter figure',path=path)
    plot_utils.save_scatter_diagram(None,x=threshold['d_c'].values,y=threshold['H'].values,x_label='delta',y_label='H',title='threshold scatter figure',path=path)

    if level=="DEBUG":
        plot_utils.plot_scatter_diagram(None,x=threshold['d_c'].values,y=threshold['H'].values,x_label='delta',y_label='H',title='threshold scatter figure')
        plot_utils.plot_scatter_diagram(None, x=threshold['H'].values, y=threshold['d_c'].values, x_label='delta',
                                        y_label='H', title='threshold scatter figure')


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