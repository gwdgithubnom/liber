"""

加载../conf目录下的配置文件:config.ini

"""

import sys,os,time,getopt
import ConfigParser

class UserConfig:
    def __init__(self, path):
        self.path = path
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.path)
    def get(self, field, key):
        result = ""
        try:
            result = self.cf.get(field, key)
        except:
            result = ""
        return result
    def set(self,section, field, key, value):
        try:
            if len(section) > 0:
                self.cf.add_section(section)
            if len(field) >0 and len(value) > 0:
                self.cf.set(field, key, value)
            self.cf.write(open(self.path,'w'))
        except:
            return False
        return True
    def remove_option(self, field,key):
        try:
            if len(key) >0 and len(field) > 0:
                self.cf.remove_option(field,key)
            self.cf.write(open(self.path,'w'))
        except:
            return False
        return True
    def remove_section(self,field):
        try:
            if len(field) >0:
                self.cf.remove_section(field)
            self.cf.write(open(self.path,'w'))
        except:
            return False
        return True

def read_config(config_file_path, field, key):
    try:
        config = UserConfig(config_file_path)
        result = config.get(field,key)
    except:
        sys.exit(1)
    return result
def write_config(config_file_path,section, field, key, value):
    try:
        config = UserConfig(config_file_path)
    except:
        return False
        #sys.exit(1)
    return True
def remove_option_config(config_file_path, field,key):
    try:
        config = UserConfig(config_file_path)
        config.remove_option(field,key)
    except:
        return False
    return True
def remove_section_config(config_file_path,field):
    try:
        config = UserConfig(config_file_path)
        config.remove_section(field)
    except:
        return False
    return True
    #def usage():
    # '''
    # opcfg.py OPTIONS:.
    # configfile c    The configuration file name
    # field  F        The name of field
    # addkey a        The adding the name key
    # getkey g        The getting the name key
    # value v         The value of key
    # add_section A   The adding the name of section
    # delkey  d       The deleteing the name of key
    # del_scetion D   The deleteting the name of section
    # help h          Get the help file
    # '''
# config = ConfigParser.ConfigParser() //初始化config实例（建立一个空的数据集实例）
# config.read(filename)  //通过load文件filename来初始化config实例
# config.get(section, key) //获得指定section中的key的value
# config.set(section, key, value)  //在指定section中，添加一对key-value键值对
# config.remove_option(section, key) //删除指定section的key
# config.remove_section(section)     //删除指定section
# config.write(open(filename,'w'))   //保存配置

if __name__ == '__main__':
    userList=UserConfig("config.ini")
    s=input("number:")
    print(userList.get("user",str(s)))