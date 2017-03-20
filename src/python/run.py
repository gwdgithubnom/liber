from tools import  image_xml_builder
from tools import logger
log=logger.getLogger()
from tools import  binaryzation_crop
from tools import  file_manage
from  tools import  image_xml_builder
from tools import  image_rebuild
from pandas import  DataFrame
d=DataFrame([],columns=['a','b'])

a={'1111','2323'}
b=['2345','2323','1']
c=['a','b']
d=d.append(DataFrame([dict(a=a,b=b)],index=['a']))
d=d.append(DataFrame([dict(a=a,b=b)],index=['b']))
d=d.append(DataFrame([dict(a=a,b=b)],index=['e']))
d=d.append(DataFrame([dict(a=a,b=b)],index=['w']))
d=d.append(DataFrame([dict(a=a,b=b)],index=['h']))
# d=d.drop(d.index[[4]])[x for j in pre for x in j])
d=d.drop(['a'])
d=[l for l1 in a for l in b]
c=DataFrame({'a':[[1, 3, 4, 5, 7, 8, 10, 11, 12, 13, 15, 16, 17]],'b':[424.0]})
pile=['a','c']
next=0
c.ix[next, 'a']=str([1,2])
log.debug(type(c.ix[next, 'a']))
d=c
import  numpy

a=DataFrame([[0,1,2],[3,4,5]],columns=['a','b','c'])
d=numpy.concatenate([a,a],axis=0)
log.debug(d)

#log.debug(((d.ix[1,'a']&set(b))))

