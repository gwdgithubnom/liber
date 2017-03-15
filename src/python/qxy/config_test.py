import configparser
import os


""""def _store_(doc_name, a):
    store = open("directory.ini", "a+")
    conf=configparser.ConfigParser()
    conf.read(store)
    list = [doc_name, '=', a]
    print(doc_name+"="+str(a)+"\n",file=store)
    conf.set("info", "b_newkey", "new-value")
    conf.add_section(section="info")
    conf.set("info","info","male")
    conf.write(open(store,"a+"))
    store.close()

    conf = configparser.ConfigParser()
    conf.read("test.cfg")

    sections = conf.sections()
    print 'sections:', sections         #sections: ['sec_b', 'sec_a']
    #得到指定section的所有option
    options = conf.options("sec_a")
    print 'options:', options           #options: ['a_key1', 'a_key2']
    #得到指定section的所有键值对
    kvs = conf.items("sec_a")
    print 'sec_a:', kvs                 #sec_a: [('a_key1', '20'), ('a_key2', '10')]
    #指定section，option读取值
    str_val = conf.get("sec_a", "a_key1")
    int_val = conf.getint("sec_a", "a_key2")

    print "value for sec_a's a_key1:", str_val   #value for sec_a's a_key1: 20
    print "value for sec_a's a_key2:", int_val   #value for sec_a's a_key2: 10

    #写配置文件
    #更新指定section，option的值
    conf.set("sec_b", "b_key3", "new-$r")
    #写入指定section增加新option和值
    conf.set("sec_b", "b_newkey", "new-value")
    #增加新的section
    conf.add_section('a_new_section')
    conf.set('a_new_section', 'new_key', 'new_value')
    #写回配置文件
    conf.write(open("test.cfg", "w"))"""
def gen_ini():
    ftest = open('directory.ini','+a')
    config_write = configparser.RawConfigParser()
    config_write.add_section('Section_a')
    config_write.add_section('Section_b')
    config_write.add_section('Section_c')
    config_write.set('Section_a','option_a1','apple_a1')
    config_write.set('Section_a','option_a2','banana_a2')
    config_write.set('Section_b','option_b1','apple_b1')
    config_write.set('Section_b','option_b2','banana_b2')
    config_write.set('Section_c','option_c1','apple_c1')
    config_write.set('Section_c','option_c2','banana_c2')
    config_write.write(ftest)
    ftest.close()


if __name__ == "__main__":
    gen_ini()

