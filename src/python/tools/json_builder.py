import  numpy
import json
from cluster.json_viewer import ClusterViwer
from context import resource_manager

def cluster_view_json_builder(clusters=[]):
            """
            将用户传入的多个json格式的对象存储在json文件中
            newlist【】作为list先读入文件中的数据以防止丢失，然后追加新加入的json对象（以list格式存入newlist）
            :param clusters:
            :return:
            """
            for c in clusters :

                if not isinstance(c, ClusterViwer):
                    raise Exception("错误的数据类型，不是ClusterViwer")
                else:
                    newlist=[]
                    try:
                        with open(resource_manager.Properties.getRootPath()+resource_manager.getSeparator()+'data'+resource_manager.getSeparator()+'json'+resource_manager.getSeparator()+'test.json','r')as R:
                            readed=json.load(R)
                        for r in readed:
                                newlist.append(r)
                    except:
                        print('The file is empty!')
                    newlist.append(c.tolist())
                    with open(resource_manager.Properties.getRootPath()+resource_manager.getSeparator()+'data'+resource_manager.getSeparator()+'json'+resource_manager.getSeparator()+'test.json','w+')as f:
                        f.write(json.dumps(newlist,skipkeys=True,sort_keys=True,indent=2))


def cluster_json_builder(clusterviwer=ClusterViwer(),x=numpy.array([]),y=numpy.array([])):
    """
    用于根据ClusterViwer类将x与y传入对象的data属性中，并将对象转换为json格式
    :param clusterviwer:[ClusterViwer(name=)]
    :param x:
    :param y:
    :return:
    """
    clusterviwer.setData(x,y)
    a=clusterviwer.toJson()
    print(a)



if __name__ == "__main__":
    c1=ClusterViwer()
    c2=ClusterViwer()
    l=[]
    l.append(c1)
    l.append(c2)
    cluster_json_builder(c1,x=numpy.array([1,2,3]),y=numpy.array([1,2,4]))
    cluster_json_builder(c2,x=numpy.array([3,3,3]),y=numpy.array([2,2,2]))
    cluster_view_json_builder(l)
