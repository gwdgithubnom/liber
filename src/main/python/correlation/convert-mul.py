from PIL import Image
filename='test.jpg'
im = Image.open(filename)
import numpy
import os
from pandas import DataFrame

x_variable=[]
y_variable=[]
path='./20x20'
p=[]
for i in os.walk(path,False):
    p=i
    break;
files=p[2]
file_count=len(files)
width, height = im.size
img = Image.open(filename)
img = img.convert("RGB")
pixdata = img.load()
rows=img.size[0]
cols=img.size[1]
pixels=numpy.zeros((file_count+1,rows))
i=0
id=[]
for filename in files:
    img = Image.open(os.path.join(path,filename))
    img = img.convert("RGB")
    pixdata = img.load()
    rows=img.size[0]
    cols=img.size[1]
    for width_x in range(img.size[0]):
        count=0
        for height_y in range(img.size[1]):
            pixel = img.getpixel((width_x, height_y))
            # print('start' + str(img.getpixel((width_x, height_y))))
            gray = pixel[0] * 0.299 + pixel[1] * 0.587 + pixel[2] * 0.114
            if (gray >10):
                # pixels[height_y][width_x]=1
                count=count+1
                # z = (255 - z) / 255 * 255
        if count%2==0:
            count=count+1
        pixels[i][width_x]=count
    id.append(filename)
    i=i+1
id.append('demo')
pixels=DataFrame(pixels,index=id)
pixels.to_csv('pixel_data-row-20x20.csv')
# numpy.savetxt("pixel_data.csv", pixels, delimiter=",")
