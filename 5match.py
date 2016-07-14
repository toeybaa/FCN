import  os, sys, operator
from collections import defaultdict, OrderedDict
from draw_result import vistop5

def five_most_sim():
    adict = OrderedDict()
    lp = sorted(os.listdir("/home/peth/Databases/rPascal/features/nDCG/"))
    for i in xrange(0, len(lp)):
        print lp[i].rstrip(".txt")
    print 'Choose a query image from above files: '
    p = raw_input('Query Image? : ')
    checker = False
    bprint = []

    if (p + ".txt") in lp and not checker:

        path = '/home/peth/Databases/rPascal/features/nDCG/' + p + '.txt'

        with open(path) as file:
            checker = True
            data = file.readlines()
            for line in data:
                word = line.split()
                adict[word[0]] = float(word[1])
            sorted_x = sorted(adict.items(), key=operator.itemgetter(1))
        #   print (sorted_x)

        for i in xrange(0,5):
            bprint.append(sorted_x[i][0])

        print bprint
        vistop5(p, bprint[0],bprint[1],bprint[2],bprint[3],bprint[4])

    if checker is False:
        print 'File not found...'

if __name__ == "__main__":
    five_most_sim()


