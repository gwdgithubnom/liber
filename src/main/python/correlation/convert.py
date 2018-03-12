from PIL import Image

filename='test-50x50.jpg'
im = Image.open(filename)
import numpy
from pandas import DataFrame
# pixels = list(im.getdata())
width, height = im.size
#imgarray=numpy.array(img)
# pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
# pixels = numpy.asarray(im)
img = Image.open(filename)
# img = img.convert("LA")
img = img.convert("RGB")
pixdata = img.load()
rows=img.size[0]
cols=img.size[1]
#scan by cols
"""
for y in range(cols):
    for x in range(rows):
        pixdata[x,y]=0  if pixdata[x,y]>=128 else 255
"""
x_variable=[]
y_variable=[]

pixels=numpy.zeros((rows,cols))
tag=0
for i in range():
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
        pixels[tag][width_x]=count
pixels=DataFrame(pixels)
pixels.to_csv('pixel_data-01.csv')
# numpy.savetxt("pixel_data.csv", pixels, delimiter=",")