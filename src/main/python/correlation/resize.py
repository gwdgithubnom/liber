from PIL import Image
import numpy
"""
auto resize the diretory image
"""
import os
path='.'
p=[]
filename=''
img = Image.open(os.path.join('1024',filename))
img = img.convert("RGB")
out = img.resize((20, 20),Image.ANTIALIAS)
out.save(filename)
