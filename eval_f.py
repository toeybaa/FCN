import numpy as np
from PIL import Image
import caffe
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from matplotlib import cm
from numpy.random import randn
# load image, switch to BGR, subtract mean, and make dims C x H x W for Caffe
im = Image.open('/home/inoue/external_data/VOCdevkit/VOCdevkit/VOC2007/JPEGImages/000001.jpg')
in_ = np.array(im, dtype=np.float32)
in_ = in_[:,:,::-1]
in_ -= np.array((104.00698793,116.66876762,122.67891434))
in_ = in_.transpose((2,0,1))
# (Caffe) Load net
net = caffe.Net('deploy.prototxt', 'fcn8s-heavy-pascal.caffemodel', caffe.TEST)
# layer name print test 
for layer_name, blob in net.blobs.iteritems():
	if 1 <= len(layer_name) <= 7 :
		print layer_name + '\t' +'\t' +'\t'+'\t'+'\t'+ str(blob.data.shape)
	elif 8 <= len(layer_name) <= 19 :
		print layer_name + '\t' +'\t'+'\t'+'\t'+ str(blob.data.shape)
	elif 20 <= len(layer_name) <= 21 :
		print layer_name + '\t' +'\t'+'\t'+ str(blob.data.shape)
	elif 22 <= len(layer_name) <= 28 :
		print layer_name + '\t' +'\t'+ str(blob.data.shape)
	else :
		print layer_name + '\t' + str(blob.data.shape)
# shape for input (data blob is N x C x H x W), set data
net.blobs['data'].reshape(1, *in_.shape)
net.blobs['data'].data[...] = in_
# run net
net.forward()
# get result from "score_fr" layer with all channels
out = net.blobs['score_fr'].data[0]
types = ['background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
def draw(input, i):
	fig, ax = plt.subplots()
	cax = ax.imshow(input, interpolation='nearest', cmap=cm.coolwarm)
	ax.set_title(types[i] + '\'s Heatmap')
	vmin = input.min()
	vmax = input.max()
	cbar = fig.colorbar(cax, ticks=[-1, 0, 1])
	cbar.ax.set_yticklabels(['< -1', '0', '> 1'])

# input = net.blobs['score_fr'].data[0]
def heatmap(input):
	# amax = [0, 12, 15]
	amax = np.unique(input.argmax(0))
	# i = 0, 12, 15
	for i in amax:
		# Draw net.blobs['score_fr'].data[0]([i])
		draw(input[i], i)
		filename = 'test_' + types[i] + '_' + str(i) + '.png'
		npysave = 'layer_' + types[i] + '.npy'
		print(filename)
		plt.savefig(filename)
		np.save(npysave, input[i])

heatmap(out)

# delete the background channel
out = out[1:,::]

# save segmentation
np.save('out.npy', out)
