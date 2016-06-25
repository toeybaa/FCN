import numpy as np

def dist_cal():
    v1 = np.load('/home/peth/Databases/rPascal/features/caffe/references/2008_003944.npy')
    v2 = np.load('/home/peth/Databases/rPascal/features/caffe/references/2008_004121.npy')
    dist = np.linalg.norm(v1-v2)
    dist2 = np.linalg.norm(v2-v1)
    print (str("d1: ") + str (dist))
#  print (str("d2: ")+ str(dist2))

dist_cal()
