import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def vispair(x1, x2):
    input = "/home/peth/Databases/rPascal/Queries/" + x1 + ".jpg"
    output = "/home/peth/Databases/rPascal/References/" + x2 + ".jpg"

    fig = plt.figure()
    for n, fname in enumerate((input, output)):
        img=mpimg.imread(fname)

        fig.add_subplot(1, 2, n)  # horizontal ori
        plt.imshow(img)
        plt.axis("off")
        plt.title('Most Similar Image'+"\n")

    plt.title('Input Image'+"\n")
    plt.show()




