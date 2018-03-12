
import json
import demjson
import  numpy
from context import resource_manager
from tools import file_manage

def json_test():

    """with open('data'+resource_manager.getSeparator()+'json'+resource_manager.getSeparator()+'cluster.json','r') as f:
        data=json.load(f)"""
    x=numpy.array([1,2,3,4,5,6,7,2,2,2,3,2,1,1])
    print(x)
if __name__ == "__main__":
    json_test();