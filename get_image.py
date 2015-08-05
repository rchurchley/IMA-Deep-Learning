import wget
import sys
import cv2

def grabImage(num_images):
    '''
    Grabs num_images images from the human_URLs.txt file

    Returns a list of filenames of the image files.
    '''
    f = open('human_URLs.txt', 'r')
    i = 0
    filenames = []

    # iterate through the defined number of image files
    for line in f:
        if i == num_images:
            break
        filenames.append(wget.download(line))
        i += 1

    return filenames


def processFile(filename):
    '''
    Performs some kind of as of yet mildly undefined processing on the photo.
    '''

    # read in via opencv
    img = cv2.imread(filename)
    rows = img.shape[0]
    cols = img.shape[1]

    # do something!

    # return something else!


if __name__ == '__main__':

    if len(sys.argv) == 1:
        num_images = 1
    else:
        num_images = int(sys.argv[1])
    filenames = grabImage(num_images)

    # do processing right here
    for f in filenames:
        f_edit = processFile(f)
