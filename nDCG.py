import PIL
import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.io as sio
import math
import operator
from collections import defaultdict, OrderedDict
from dataset import dist_cal
import glob

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
    #    convert(r)
        labeld = self.annotations
        avgDCG(r, labeld)

# Write the file of all reference images based on the user string keyboard input of the query
def anconvert(d, l, inpath):
  #  print inpath
    path = '/home/peth/Databases/rPascal/features/caffe/queries/'
    finput = inpath + '.npy'
    check = True
    isfile = glob.glob("/home/peth/Databases/rPascal/features/nDCG/*.txt")
    if len(isfile) == 50:
        check = False
        return tosort(inpath, l)
    if check:
        for fname in sorted(os.listdir(path)):
            if finput == fname:
                file = open("/home/peth/Databases/rPascal/features/nDCG/" + inpath + ".txt", 'w')
                for key in d:
                    # print key
                    if inpath == key:
                        value = d[key]
                        for element in value:
                            dist = str(dist_cal(key, element))
                            ref = str(element).rstrip(".jpg")
                            file.write(ref)
                            file.write(" ")
                            file.write(dist)
                            file.write("\n")
                file.close()
                print 'All reference and distance of ' + str(inpath) + " is written"
        return tosort(inpath, l)


# Sort the distance (in ascending order) based on the previous input by the user
def tosort(path, l):
    adict = OrderedDict()
    with open("/home/peth/Databases/rPascal/features/nDCG/" + path + ".txt") as file:
        data = file.readlines()
        for line in data:
            word = line.split()
            adict[word[0]] = float(word[1])

        sdict = OrderedDict(sorted(adict.items(), key=operator.itemgetter(1)))
    list = []
    for key in sdict:
        e = (l[path][key])
        #    print key, '........', sdict[key], e
        list.append(e)
    # main(list)

    return reallist(list, path)


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
        print "Processing query: " + (query) + " <=> Most similar image is: " + (min_y) + " <=> Distance is: " + str(min_dist)
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

    # Arjun's Implementation
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

#Draw the example of 4 images in the format of query and label (0, 1, 2, 3)
def visualize_dataset(dset):
    fig = plt.figure()
    plt.axis("off")
    plt.tight_layout()

    key = dset.queries.keys()[np.random.randint(50)]
    dset.queries[key].load_to_figure(fig.add_subplot(1, 5, 1), "query")
    for i in reversed(range(4)):
        for name, label in dset.annotations[key].items():
            if label == i:
                dset.references[name].load_to_figure(fig.add_subplot(1, 5, i + 2), i)
                break
    plt.show()
    plt.savefig("good.png")

#Find average DCG for all query images and print it @ the specify k value
def avgDCG(d, l):
    alist = []
    path = '/home/peth/Databases/rPascal/features/caffe/queries/'
    for fname in sorted(os.listdir(path)):
        alist.append(anconvert(d, l, fname.rstrip('.npy')))
    print sum(alist) / len(alist)


#List creation for nDCG calculation, printing also
def reallist(list, path):
    real = list
#    print real
#    print len(real)
    gt = sorted(real, reverse=True)
    # k = len(real)
 #   each = "nDCG value of",path,"is", dcg(real, k=10) / dcg(gt, k=10)
    value = dcg(real, k=30) / dcg(gt, k=30)
    return value

#nDCG calculation method
def dcg(rank_list, k=None):
    if k is None:
        k = len(rank_list)
    sum = 0
    for i, rank in enumerate(rank_list):
        if k <= i:
            break
        # there is something wrong with nDCG in the paper
        # https://crowdsolving.jp/node/1435
        sum += (math.pow(2, rank) - 1) / math.log(i + 2, 2)
    return sum

def main():
    dset = Dataset(RPASCAL_DIR)
    # Dataset dset = Dataset.getInstance(RPASCAL_DIR)
    # visualize_dataset(dset)
    # dset = Dataset.__new__(cls, ****)
    # dset.__init__(RPASCAL_DIR)
    #  for key, values in dset.annotations.items():
    #      print key

if __name__ == "__main__":
    main()

