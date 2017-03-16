"""
Created on 2016-09-13
Create a xml file
@author: gwd
"""
from tools import logger
from xml.dom import minidom
from PIL import Image
from xml.dom import minidom
import numpy as np
from context import resource_manager
import os
import xml.etree.ElementTree
log=logger.getLogger()

def addImageNode(document=minidom.Document(),id=str(0),data=str(0)):
    image=document.createElement("Image")
    id=document.createElement("Id")
    data=document.createElement("Data")
    id.appendChild(document.createTextNode(id))
    data.appendChild(document.createTextNode(data))
    image.appendChild(id)
    image.appendChild(data)


class pcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    Blue='\34[95m'
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def dir_to_dataset(path):
    #print("Gonna process:\n\t %s"%path)
    log.info("start working LA operation in directory"+path)
    if not os.path.exists(path):
        log.error("error path"+path)
    dataset = []
    #for file_count, file_name in enumerate( sorted(glob(glob_files),key=len) ):
    subdir=os.listdir(path)
    for dir in subdir:
        if os.path.isdir(os.path.join(path,dir)):
            #print("start read director "+os.path.join(path,dir))
            dataset.extend(dir_to_dataset(os.path.join(path,dir)))
        elif os.path.isfile(os.path.join(path,dir)):
            filename=os.path.join(path,dir)
            #print("read file:"+filename)
            #image = Image.open(dir)
            try:
                img = Image.open(filename).convert('LA') #tograyscale
            except:
                os.remove(filename)
                log.warn("wrong file in this directory"+filename+". and delete the file.")
            pixels = [f[0] for f in list(img.getdata())]
            filename=os.path.basename(dir)
            #print(filename[0:-4])
            #pixels.append(int(filename[0:-4]))
            pixels.insert(0,(filename[0:-4]))
            dataset.append(pixels)
    return dataset
"""
for this method update at 20160913 to add new code to support to create image.xml
http://www.cnblogs.com/wangshide/archive/2011/10/29/2228936.html
http://www.cnblogs.com/xiaowuyi/archive/2012/10/17/2727912.html
http://www.cnblogs.com/coser/archive/2012/01/10/2318298.html
"""
def initDataSet(source=resource_manager.Properties.getDefaultOperationFold(),path=resource_manager.Properties.getImageXmlResource()):
    rmfile()
    log.info("starting to init dataset to running create image.xml module.")
    #path="D:\Projects\\Python\\deeplay\\src\\train\\run\\*";
    Data= dir_to_dataset(source)
    Data=np.array(Data)
    # Data and labels are read
    #set a filename
    afileName = str(os.getcwd()) + resource_manager.getSeparator()+"kmeans.data"
    #create the file
    file = open(afileName, 'w')
    #put the data into a file.
    #print(len(Data))
    xmlFile=str(os.getcwd())+resource_manager.getSeparator()+"image1.xml"
    log.info("starinng to build image xml file")
    if(os.path.exists(xmlFile)==False):
        document=minidom.Document()
        document.appendChild(document.createComment("this is used for save a image file"))
        imagelist=document.createElement("Images")
        document.appendChild(imagelist)
        f=open(path,"w")
        document.writexml(f,addindent=' '*4, newl='\n', encoding='utf-8')
        f.close()
    root=xml.dom.minidom.parse(path)
    imagesRoot=root.documentElement
    #root=xml.etree.ElementTree.parse("image.xml");
    for x in range(0, len(Data)):
        imageRoot=document.createElement("Image")
        id=document.createElement("id")
        data=document.createElement("data")
        aRow = Data[x]
        value=[]
        for pix in range(1, len(aRow)):
            file.write(str(aRow[pix]))
            value.append(int(str(aRow[pix])))
            if pix != len(aRow) - 1:
                file.write(",")
        #print(len(aRow))
        id.appendChild(document.createTextNode(aRow[0]))
        data.appendChild(document.createTextNode(str(value)))
        imagesRoot.appendChild(imageRoot)
        imageRoot.appendChild(id)
        imageRoot.appendChild(data)
        file.write("\n")
    f=open(path,"w")
    root.writexml(f,addindent=' '*4, newl='\n', encoding='utf-8')
    f.close()

def rmfile(xmlFile=resource_manager.Properties.getImageXmlResource()):
    try:
        os.remove(xmlFile)
    except:
        log.info("do not found image xml  file "+xmlFile+", create a new image xml.")


def imageBuildXml(data):
    """
    this is used for build xml fil
    e to save to java.
    :param data:
    :return:
    """
    """
    document=minidom.Document()
    document.appendChild(document.createComment("this is used for save a image file"))
    imagelist=document.createElement("Images")
    document.appendChild(imagelist);
    """



def build_image_xml(source=resource_manager.Properties.getDefaultOperationFold(),path=resource_manager.Properties.getImageXmlResource()):
    rmfile(path)
    initDataSet(source,path)


from xml.etree.ElementTree import ElementTree,Element

def read_xml(in_path):
    '''读取并解析xml文件
      in_path: xml路径
      return: ElementTree'''
    tree = ElementTree()
    tree.parse(in_path)
    return tree

def write_xml(tree, out_path):
    '''将xml文件写出
      tree: xml树
      out_path: 写出路径'''
    tree.write(out_path, encoding="utf-8",xml_declaration=True)

def if_match(node, kv_map):
    '''判断某个节点是否包含所有传入参数属性
      node: 节点
      kv_map: 属性及属性值组成的map'''
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True

#---------------search -----
def find_nodes(tree, path):
    '''查找某个路径匹配的所有节点
      tree: xml树
      path: 节点路径'''
    return tree.findall(path)

def get_node_by_keyvalue(nodelist, kv_map):
    '''根据属性及属性值定位符合的节点，返回节点
      nodelist: 节点列表
      kv_map: 匹配属性及属性值map'''
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes

#---------------change -----
def change_node_properties(nodelist, kv_map, is_delete=False):
    '''修改/增加 /删除 节点的属性及属性值
      nodelist: 节点列表
      kv_map:属性及属性值map'''
    for node in nodelist:
        for key in kv_map:
            if is_delete:
                if key in node.attrib:
                    del node.attrib[key]
            else:
                node.set(key, kv_map.get(key))

def change_node_text(nodelist, text, is_add=False, is_delete=False):
    '''改变/增加/删除一个节点的文本
      nodelist:节点列表
      text : 更新后的文本'''
    for node in nodelist:
        if is_add:
            node.text += text
        elif is_delete:
            node.text = ""
        else:
            node.text = text

def create_node(tag, property_map, content):
    '''新造一个节点
      tag:节点标签
      property_map:属性及属性值map
      content: 节点闭合标签里的文本内容
      return 新节点'''
    element = Element(tag, property_map)
    element.text = content
    return element

def add_child_node(nodelist, element):
    '''给一个节点添加子节点
      nodelist: 节点列表
      element: 子节点'''
    for node in nodelist:
        node.append(element)

def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
    '''同过属性及属性值定位一个节点，并删除之
      nodelist: 父节点列表
      tag:子节点标签
      kv_map: 属性及属性值列表'''
    for parent_node in nodelist:
        children = parent_node.getchildren()
        for child in children:
            if child.tag == tag and if_match(child, kv_map):
                parent_node.remove(child)
"""
if __name__ == "__main__":
    #1. 读取xml文件
    tree = read_xml("./test.xml")

    #2. 属性修改
    #A. 找到父节点
    nodes = find_nodes(tree, "processers/processer")
    #B. 通过属性准确定位子节点
    result_nodes = get_node_by_keyvalue(nodes, {"name":"BProcesser"})
    #C. 修改节点属性
    change_node_properties(result_nodes, {"age": "1"})
    #D. 删除节点属性
    change_node_properties(result_nodes, {"value":""}, True)

    #3. 节点修改
    #A.新建节点
    a = create_node("person", {"age":"15","money":"200000"}, "this is the firest content")
    #B.插入到父节点之下
    add_child_node(result_nodes, a)

    #4. 删除节点
    #定位父节点
    del_parent_nodes = find_nodes(tree, "processers/services/service")
    #准确定位子节点并删除之
    target_del_node = del_node_by_tagkeyvalue(del_parent_nodes, "chain", {"sequency" : "chain1"})

    #5. 修改节点文本
    #定位节点
    text_nodes = get_node_by_keyvalue(find_nodes(tree, "processers/services/service/chain"), {"sequency":"chain3"})
    change_node_text(text_nodes, "new text")

    #6. 输出到结果文件
    write_xml(tree, "./out.xml")
"""
if __name__=="__main__":
    log.info("starting building image xml.")
    rmfile()
    initDataSet()
