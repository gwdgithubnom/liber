from PIL import Image
file='test.jpg'
tofile='test-10x10.jpg'
im = Image.open(file)
out = im.resize((10, 10),Image.ANTIALIAS)
out.save(tofile)