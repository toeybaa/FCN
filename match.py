import sys, os
from drawtest import vispair

def main():
    path = raw_input("Please type the image name in query folder: ")
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
                print "Query Image is: " + str(word[0]) + " <==> Most similar Image is: " + str(word[1])
                break
        if checker is False:
            print "File not found, Exiting the program..."

if __name__ == "__main__":
    main()