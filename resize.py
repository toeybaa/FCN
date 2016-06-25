from PIL import Image
import os, sys
import numpy as np

def resize():
        for item in dirs:
                if os.path.isfile(path+item):
                        print (path)
                        print (item)
                        print (path+item)
                        im = Image.open (path+item)
                        f, e = os.path.splitext(path+item)
                        imResize = im.resize((320,320), Image.ANTIALIAS)
                        # imResize.save (f+'resized.jpg','JPEG',quality = 90)
                        np.save(f, imResize)

path = "/home/peth/Databases/rPascal/Queries/"
dirs = os.listdir(path)

resize()

path = "/home/peth/Databases/rPascal/References/"
dirs = os.listdir(path)

resize()

path = "/home/peth/Databases/rPascal/Queries/"
cdirs = os.listdir(path)

def make_caffe():
    print ("Method Called")
    for item in cdirs:
        if os.path.isfile(path+item):
            f, e = os.path.splitext(path+item)
            im = Image.open(path+item)
            in_ = np.array(im, dtype=np.float32)
            in_ = in_[:, :, ::-1]
            in_ -= np.array((104.00698793, 116.66876762, 122.67891434))
            in_ = in_.transpose((2, 0, 1))
            net = caffe.Net('deploy.prototxt', 'fcn8s-heavy-pascal.caffemodel', caffe.TEST)
            net.blobs['data'].reshape(1, *in_.shape)
            net.blobs['data'].data[...] = in_
            net.forward()
            out = net.blobs['score_fr'].data[0]
            np.save(f, out)
            print (str("Item Saved: ")+item)

