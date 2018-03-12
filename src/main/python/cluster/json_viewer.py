import json
import  numpy
from context import resource_manager

class ClusterViwer(object):
        """
        https://my.oschina.net/pangyangyang/blog/200329
        用于配置ClusterViewer的Json视图
        """
        def  __init__(self,name='undefine',type='cluster',large='true',symbol='circle',symbolSize=12,label='',data='',itemStyle=''):
                self.name = name
                self.type = type
                self.large = large
                self.symbol = symbol
                self.symbolSize = symbolSize
                self.lablel = label
                self.data = data
                self.itemStyle=itemStyle

        def setData(self,x,y):
                """
                将用户传入对象的numpy.array数组存入data属性中
                :return:
                """
                x=numpy.ndarray.tolist(x)
                y=numpy.ndarray.tolist(y)
                list={}
                data=[]
                c=0
                for a,b in zip(x,y):
                        list["x"]=a
                        list["y"]=b
                        data.append(list)
                        list={}
                        c=c+1

                self.data=data

        def toJson(self):
                """
                返回支持json序列化的对象
                :return:
                """
                list={}
                list['name']=self.name
                list['type']=self.type
                list['large']=self.large
                list['symbolSize']=self.symbolSize
                list['data']=self.data
                outlist=[list]
                return json.dumps(outlist,skipkeys=True,sort_keys=True,indent=2)

        def tolist(self):
                """
                返回对象相对应的字典方便存储在文件中
                :return:
                """
                list={}
                list['name']=self.name
                list['type']=self.type
                list['large']=self.large
                list['symbolSize']=self.symbolSize
                list['data']=self.data
                return list





