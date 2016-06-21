from PIL import Image
import os, sys
path = "/home/peth/Databases/rPascal/References/"
dirs = os.listdir(path)

def resize():
	for item in dirs:
		if os.path.isfile(path+item):
			im = Image.open (path+item)
			f, e = os.path.splitext(path+item)
			imResize = im.resize((320,320), Image.ANTIALIAS)
			# imResize.save (f+'resized.jpg','JPEG',quality = 90)
			np.save(f, imResize)

resize()
