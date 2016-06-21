import numpy as np
from PIL import Image
import caffe

# load image, switch to BGR, subtract mean, and make dims C x H x W for Caffe
# im = Image.open('pascal/VOC2010/JPEGImages/2007_000129.jpg')
im = Image.open('/home/inoue/external_data/VOCdevkit/VOCdevkit/VOC2007/JPEGImages/000001.jpg')
in_ = np.array(im,dtype=np.float64)
in_ = in_[:,:,::-1]
in_ -= np.array((104.00698793,116.66876762,122.67891434))
in_ = in_.transpose((2,0,1))

# load net
#net = caffe.Net('deploy.prototxt', 'fcn-32s-pascalcontext.caffemodel', caffe.TEST)
net = caffe.Net('deploy.prototxt', 'fcn8s-heavy-pascal.caffemodel', caffe.TEST)
# shape for input (data blob is N x C x H x W), set data
net.blobs['data'].reshape(1, *in_.shape)
net.blobs['data'].data[...] = in_
# run net and take argmax for prediction
net.forward()
out = net.blobs['score_fr'].data[0][15]

import matplotlib.pyplot as plt
plt.switch_backend('agg')
from matplotlib import cm

fig, ax = plt.subplots()
cax = ax.imshow(out, interpolation='nearest', cmap=cm.coolwarm)
ax.set_title('Person\'s Heatmap')
cbar = fig.colorbar(cax, ticks=[0, 30.69, 31])
cbar.ax.set_yticklabels(['0', '30.69', '31'])
out = out[1:,::]
#print(data[0])
#out = net.blobs['score'].data[0].argmax(axis=0)
# save prediction
np.save('out.npy', out)
plt.show()

# save as image
#palette_base = [i for i in xrange(0, 256, 255 / 3)]
#palette = [(palette_base[i], palette_base[j] , palette_base[k]) for i in xrange(4) for j in xrange(4) for k in xrange(4)]
#colors = np.array(palette, dtype=np.uint8)[out]
#Image.fromarray(colors).save('out.png', 'PNG')
