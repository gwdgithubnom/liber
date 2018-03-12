"""

加载../conf目录下的配置文件:config.ini

"""
class properties:
    """
    定义一个类，读取配置文件的类
    另外读取当前项目根目录
    """


"""
    walk through a directory and get all the file in this directory.
"""


def subfilesName(directory):
    fl = []
    subdir=os.listdir(directory)
    """
    for i in os.walk(path, False):
        for f in i[2]:
            fl.append(f)
    """
    for i in subdir:
        path=os.path.join(directory,i)
        print(path)
        if os.path.isdir(path):
            fl.extend(subfilesName(path))
        elif os.path.isfile(path):
            fl.append(path)
            print("add"+path)
    return fl
