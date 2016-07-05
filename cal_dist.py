import numpy as np

def dist_cal(path1, path2):
    c1 = np.load(path1)
    c2 = np.load(path2)
    dist = np.linalg.norm(c1-c2)
    # print dist
    print (str("Distance is ") + str (dist))
    # print (str("d2: ")+ str(dist2)) # the same value

#v1 = input("Input first image directory: ")
v1 = '/home/peth/Databases/rPascal/features/caffe/references/2008_008392.npy'
print (str("path 1 is: ")+str(v1))
v2 = '/home/peth/Databases/rPascal/features/caffe/references/2008_008395.npy'
#v2 = input("Input second image directory: ")
print (str("path 2 is: ")+str(v2))

dist_cal(v1,v2)
