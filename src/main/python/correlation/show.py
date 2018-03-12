from PIL import Image
import os
import matplotlib.pyplot as plt
def description(filename):
    #print "Processing ... ", fileName
    if filename == '':
        return
        #only process the jpg file
    #    sufix = os.path.splitext(fileName)[1][1:]
    #    if sufix != 'jpg':
    #        return

    #load background
    backGround = Image.open('back.jpg')
    backGround = backGround.convert('RGBA')

    #print fileName;
    #open the image
    #img = Image.open(fileName)
    #img = img.covert("RGB")
    img=backGround
    try:
        img = Image.open(filename)
        # img = img.convert("LA")
        img = img.convert("RGB")
    except:
        os.remove(filename)
        print("wrong file in this directory "+filename+". and delete the file.")
        exit
    pixdata = img.load()
    rows=img.size[0];
    cols=img.size[1];
    #scan by cols
    """
    for y in range(cols):
        for x in range(rows):
            pixdata[x,y]=0  if pixdata[x,y]>=128 else 255
    """
    x_variable=[]
    y_variable=[]
    for width_x in range(img.size[0]):
        x_count=0
        y_count=0
        for height_y in range(img.size[1]):
            pixel = img.getpixel((width_x, height_y))
            # print('start' + str(img.getpixel((width_x, height_y))))
            gray = pixel[0] * 0.299 + pixel[1] * 0.587 + pixel[2] * 0.114
            if (gray < 140):
                x_count=x_count+1
            else:
                y_count=y_count+1
                # z = (255 - z) / 255 * 255
        x_variable.append(x_count)
        y_variable.append(width_x)

        # plot_utils.plot_image_file(img)
        #print "......#####",fileName,"######....."

description(filename='test.jpg')


""""
    #crop the image to 100 * 100
    if rows != 100 and cols != 100:
        box = (0,0, rows,cols)
        region = img.crop(box)
        positioin = (int((100-rows)/2), int((100-cols)/2), int((100-rows)/2+rows), int((100-cols)/2+cols) )
        #print positioin
        backGround.paste(region,positioin)
        img = backGround
"""