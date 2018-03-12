from PIL import Image
import numpy
"""
auto resize the diretory image
"""
import os
path='./20x20/'
p=[]
for i in os.walk(path,False):
    p=i
    break;
files=p[2]
for filename in files:
    img = Image.open(os.path.join(path,filename))
    img = img.convert("RGB")
    out = img.resize((20, 20),Image.ANTIALIAS)
    out.save(path+filename)
