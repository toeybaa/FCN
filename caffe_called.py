import caffe
import numpy as np
import os, sys
from PIL import Image

def make_caffe(where):
    cdirs = os.listdir(where)
    print ("Method Called")
    for item in cdirs:
        if os.path.isfile(path+item) and item.endswith('.jpg'):
            f, e = os.path.splitext(path+item)
            print (str("Loading item: ")+f)
            im = Image.open(path+item)
            im = im.resize((320, 320), Image.ANTIALIAS)
            in_ = np.array(im, dtype=np.float32)
            in_ = in_[:, :, ::-1]
            in_ -= np.array((104.00698793, 116.66876762, 122.67891434))
            in_ = in_.transpose((2, 0, 1))
            net = caffe.Net('deploy.prototxt', 'fcn8s-heavy-pascal.caffemodel', caffe.TEST)
            net.blobs['data'].reshape(1, *in_.shape)
            net.blobs['data'].data[...] = in_
            caffe.set_mode_gpu();
            net.forward()
            out = net.blobs['score_fr'].data[0]
            np.save(f, out)
            print (str("Item Saved: ")+item)

#path = "/home/peth/Databases/rPascal/References/"

path = input("Where to run?: ")
make_caffe(path)