import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def vispair(x1, x2):
    input = "/home/peth/Databases/rPascal/Queries/" + x1 + ".jpg"
    output = "/home/peth/Databases/rPascal/References/" + x2 + ".jpg"

    fig = plt.figure()
    for n, fname in enumerate((input, output)):
        img = mpimg.imread(fname)

        ax = fig.add_subplot(1, 2, n)  # horizontal ori
        plt.imshow(img)
        plt.axis("off")
        plt.title('Most Similar Image'+"\n"+"(reference)")

    plt.title('Input Image'+"\n"+"(query)")
    plt.savefig("/home/peth/Databases/rPascal/features/images_result/" + str(x1) + "_" + str(x2) + ".png")
    plt.show()



def vistop5(x1, y1, y2, y3, y4, y5):
    input = '/home/peth/Databases/rPascal/Queries/' + x1 + '.jpg'
    out1 = '/home/peth/Databases/rPascal/References/' + y1 + '.jpg'
    out2 = '/home/peth/Databases/rPascal/References/' + y2 + '.jpg'
    out3 = '/home/peth/Databases/rPascal/References/' + y3 + '.jpg'
    out4 = '/home/peth/Databases/rPascal/References/' + y4 + '.jpg'
    out5 = '/home/peth/Databases/rPascal/References/' + y5 + '.jpg'

    fig = plt.figure()
    for n, fname in sorted(enumerate((input,out1,out2,out3,out4,out5))):
        img = mpimg.imread(fname)
        ax = fig.add_subplot(3, 2, n+1)
        if n == 0:
            plt.title("Query Image")
            plt.imshow(img)
            plt.axis("off")
        if n > 0:
            plt.title('#'+ str(n))
            plt.imshow(img)
            plt.axis("off")

    plt.show()
