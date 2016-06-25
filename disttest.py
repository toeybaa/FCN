from __future__ import division
import sys
import numpy as np
from scipy.spatial.distance import cdist

#...............................................................................
dim = 10
nx = 1000
ny = 100
metric = "euclidean"
seed = 1

    # change these params in sh or ipython: run this.py dim=3 ...
for arg in sys.argv[1:]:
    exec( arg )
np.random.seed(seed)
np.set_printoptions( 2, threshold=100, edgeitems=10, suppress=True )

title = "%s  dim %d  nx %d  ny %d  metric %s" % (
        __file__, dim, nx, ny, metric )
print "\n", title

#...............................................................................
X = np.random.uniform( 0, 1, size=(nx,dim) )
Y = np.random.uniform( 0, 1, size=(ny,dim) )
dist = cdist( X, Y, metric=metric )  # -> (nx, ny) distances
#...............................................................................

print "scipy.spatial.distance.cdist: X %s Y %s -> %s" % (
        X.shape, Y.shape, dist.shape )
print "dist average %.3g +- %.2g" % (dist.mean(), dist.std())
print "check: dist[0,3] %.3g == cdist( [X[0]], [Y[3]] ) %.3g" % (
        dist[0,3], cdist( [X[0]], [Y[3]] ))