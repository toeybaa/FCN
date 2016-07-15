import PIL
import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.io as sio
import math
import operator
from collections import defaultdict, OrderedDict

RPASCAL_DIR = "/home/peth/Databases/rPascal"
# RIMAGENET_DIR = "/home/peth/Databases/rImageNet"
IM_EXT = '.jpg'  # type of the extension of the images


class Image(object):
    def __init__(self, name, path, datatype):
        self.name = name  # like 2008_007735
        self.path = path
        self.datatype = datatype  # 'query' or 'reference'

    def load_to_figure(self, ax, title=None):
        im = np.asarray(PIL.Image.open(self.path))
        ax.imshow(im, aspect='equal')
        if title is not None:
            ax.set_title(title)
        ax.axis('off')

class Dataset(object):
    __instance = None

    def __new__(cls, *args, **keys):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)  # {}
            return cls.__instance

    def __init__(self, home_dir):
        self.home_dir = home_dir
        self.query_dir = self.home_dir + "/Queries"
        self.reference_dir = self.home_dir + "/References"
        self.corrspd_dir = self.home_dir + "/Reference_Lists"
        self.references = OrderedDict()
        self.queries = OrderedDict()
        self.annotations = defaultdict(dict)

        for fname in sorted(os.listdir(self.reference_dir)):
            if IM_EXT in fname:
                #   print "Before", fname
                name = fname.rstrip(IM_EXT)
                #   print "After", name
                self.references[name] = Image(
                    name=name,
                    path=self.reference_dir + "/" + fname,
                    datatype="reference"
                )
        for fname in sorted(os.listdir(self.query_dir)):
            if IM_EXT in fname:
                name = fname.rstrip(IM_EXT)
                self.queries[name] = Image(
                    name=name,
                    path=self.query_dir + "/" + fname,
                    datatype="query"
                )

        ann_lables = sio.loadmat(self.home_dir + "/MedianAnnot.mat")['medAnnot']
        r = OrderedDict()

        for i, name in enumerate(self.queries.keys()):
            correspondence = sio.loadmat(self.corrspd_dir + "/" + name + "_refs.mat")["refNames"]
            r[name] = correspondence
            assert len(correspondence) == ann_lables[i][0].shape[0]
            for j in range(len(correspondence)):
                self.annotations[name][correspondence[j].rstrip(IM_EXT)] = ann_lables[i][0][j][0]
        convert(r)

#Calculate/Find the most similar pair of each of all queries
def convert(d):
    print "Processing all images in dataset... "
    dict = OrderedDict()
    dict2 = OrderedDict()
    for key in d:
        value = d[key]
        min_dist = dist_cal(key, value[0])
        min_y = str(value[0])
        for element in value:
            dist = dist_cal(key, element)
            if dist <= min_dist:
                query = str(key)
                min_dist = dist
                min_y = str(element).rstrip(".jpg")
        print "Processing query: " + query + " <=> Most similar image is: " + (
            min_y) + " <=> Distance is: " + str(min_dist)
        dict[query] = min_y
        dict2[query] = str(min_dist)
    # print dict
    print "Dataset processing finished... "
    savepair(dict)
    savedist(dict2)
    print "Dataset successfully created. "

#Save the pair of query and minimum distance reference (Most similar image)
def savepair(self):
    print "Saving minimum query, reference pairs... "
    file = open("/home/peth/Databases/rPascal/most_similar_pair.txt", 'w')
    for k,v in self.items():
        file.write(k)
        file.write(" ")
        file.write(v)
        file.write("\n")
    file.close()
    print "Saved..."

#Save the pair of query and the value of minimum distance of its pair
def savedist(self):
    print "Saving the distance of queries... "
    file = open('/home/peth/Databases/rPascal/dist_pair.txt', 'w')
    for k, v in self.items():
        file.write(k)
        file.write(' ')
        file.write(v)
        file.write("\n")
    file.close()
    print "Saved.."


     #   print "min_dist_of_key: " + query + " <> " + min_y + " => dist: " + str(min_dist)
    # for e1 in k.keys():
    #     min_dist = 10000
    #     e2 = k[e1]
    #     x1 = ''
    #     x2 = ''
    #     for i in xrange(0, len(e2) - 1):
    #         count += 1
    #         new = dist_cal(str(e1), str(e2[i]))
    #         if new < min_dist:
    #             min_dist = new
    #             x1 = str(e1)
    #             x2 = str(e2[i]).rstrip(".jpg")
    #             #   print "The minimum distance is " + str (min_dist)
    #             print "Query Image is:", x1 + ",", "Most similar image is:", x2, "With the distance is:", min_dist
    #
    #             # print count

# Distance calculation method, return distance in float datatype
def dist_attcal(path1, path2):
    path1 = '/home/peth/Databases/rPascal/features/attribute_data/queries/' + path1 + '.npy'
    path2 = '/home/peth/Databases/rPascal/features/attribute_data/references/' + path2 + '.npy'
    c1 = np.load(path1)
    c2 = np.load(path2)
    distatt = np.linalg.norm(c1 - c2)
    return distatt

def dist_365cal(path1, path2):
    #dist_attcal(path1, path2)
    path1 = '/home/peth/places365/feature/query_np/' + path1 + '.npy'
    path2 = '/home/peth/places365/feature/reference_np/' + path2 + '.npy'
    c1 = np.load(path1)
    c2 = np.load(path2)
    dist365 = np.linalg.norm(c1 - c2)
    return dist365

def dist_cal(path1, path2):
    path2 = path2.rstrip(".jpg")
    d365 = dist_365cal(path1, path2)
    datt = dist_attcal(path1, path2)
    path1 = "/home/peth/Databases/rPascal/features/caffe/queries/" + path1 + ".npy"
    path2 = "/home/peth/Databases/rPascal/features/caffe/references/" + path2 + ".npy"
    c1 = np.load(path1)
    c2 = np.load(path2)
    dist = np.linalg.norm(c1 - c2)
    fdist = (0.2*dist) + (0.3*d365) + (0.5*datt)
    # # print dist
    #    print (str("Distance is ") + str (dist))
    return fdist
    # # print (str("d2: ")+ str(dist2)) # the same value

#Draw the example of 4 images in the format of query and label (0, 1, 2, 3)
def visualize_dataset(dset):
    fig = plt.figure()
    plt.axis("off")
  #  plt.tight_layout()

    key = dset.queries.keys()[np.random.randint(50)]
    dset.queries[key].load_to_figure(fig.add_subplot(1, 5, 1), "query")
    for i in reversed(range(4)):
        for name, label in dset.annotations[key].items():
            if label == i:
                dset.references[name].load_to_figure(fig.add_subplot(1, 5, i + 2), i)
                break
    plt.show()
    plt.savefig("good.png")

def main():
    dset = Dataset(RPASCAL_DIR)
    # Dataset dset = Dataset.getInstance(RPASCAL_DIR)
 #   visualize_dataset(dset)
    # dset = Dataset.__new__(cls, ****)
    # dset.__init__(RPASCAL_DIR)
    #  for key, values in dset.annotations.items():
    #      print key

if __name__ == "__main__":
    main()
