from tools import  image_xml_builder
from tools import logger
log=logger.getLogger()
from tools import  binaryzation_crop
from tools import  file_manage
from  tools import  image_xml_builder
from tools import  image_rebuild
from pandas import  DataFrame
d=DataFrame([],columns=['a','b'],index=[1,2])

a={'1111','2323'}
b=['2345','2323','1']
a.add('sdsd')
a.remove('1111')
d.ix[1,'a']=a
d.ix[333,'b']=b
log.debug(len(a))
log.debug(((d.ix[1,'a']&set(b))))

