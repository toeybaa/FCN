import sys, os
from drawtest import vispair

def pair():
    a = sorted(os.listdir('/home/peth/Databases/rPascal/features/caffe/queries/'))
    for i in xrange(0,len(a)):
        print a[i].rstrip(".npy")

    print 'Choose a query image rom above files...'
    path = raw_input("Query Image? : ")
    with open("/home/peth/Databases/rPascal/most_similar_pair.txt") as file:
        checker = False
        data = file.readlines()
        for line in data:
            word = line.split()
            if word[0] == path and not checker:
                    # print word[1]
                    # print type(word[1])
                print "Query founded, Showing the result via X-Server"
                vispair(str(word[0]), str(word[1]))
                checker = True
             #   print "Query Image is: " + str(word[0]) + " <==> Most similar Image is: " + str(word[1])
                dist(str(word[0]),str(word[1]))
                break
        if checker is False:
            print "File not found, Exiting the program..."

def dist(q, r):
    with open('/home/peth/Databases/rPascal/dist_pair.txt') as file:
        data = file.readlines()
        for line in data:
            word = line.split()
            if word[0] == q:
                print "Query Image is: " + q + " <==> Most similar Image is: " + r + " <==> Distance is: " + word[1]


if __name__ == "__main__":
    pair()
