import cv2
import sys
import numpy.random as rand


'''
Set of tools for editing any number of images in various ways.
Currently the following tools are implemented:

    - cropping all images to a specified pixel height/width
      (crops to the center)
    - adding a white line of a random thickness between two
      random points
'''


def autocrop(filename, outfile, out_height=300, out_width=300):
    '''
    Automatically crop an image to a desired height and width, saves to
    an outfile.
    '''

    img = cv2.imread(filename)
    rows = img.shape[0]
    cols = img.shape[1]
    horiz_border = (rows - out_height) / 2.
    vert_border = (cols - out_width) / 2.
    cropped_img = img[horiz_border:rows - horiz_border,
                      vert_border:cols - vert_border]
    print outfile
    cv2.imwrite(outfile, cropped_img)


def add_random_line(filename, outfile, max_thickness=40,
                    min_thickness=10):

    # open file via opencv and retrieve information
    img = cv2.imread(filename)
    rows = img.shape[0]
    cols = img.shape[1]

    # define random coordinates and thickness
    x1 = rand.randint(0, rows)
    y1 = rand.randint(0, cols)
    x2 = rand.randint(0, rows)
    y2 = rand.randint(0, cols)
    thickness = rand.randint(min_thickness, max_thickness)

    # draw the line and save the image
    cv2.line(img, (x1, y1), (x2, y2), color=(255, 255, 255),
             thickness=thickness)
    cv2.imwrite(outfile, img)


def usage(action):
    '''
    Print usage for a specific action keyword.
    '''
    print 'Usage:'
    if action == 'crop':
        print 'python pic_tools.py crop [height] [width] ' \
            + '[-option] [input filenames]...'
        print 'Options: i for editing in place, otherwise creates new files'

    if action == 'line':
        print 'python pic_tools.py line [min_thickness] [max_thickness] ' \
            + '[-option] [input filenames]...'
        print 'Options: i for editing in place, otherwise creates new files'


if __name__ == '__main__':

    # perform actions on a large set of images based on command line keyword
    argc = len(sys.argv)
    if argc == 1:
        print 'Error: must add an action command line argument!'
        print 'Options so far: crop'
        sys.exit(1)

    action = sys.argv[1]

    if action == 'line':

        # check for appropriate usage
        if argc < 5:
            print 'Error: insufficient command line arguments!'
            usage(action)
            sys.exit(1)

        # load in thicknesses
        try:
            min_thick = int(sys.argv[2])
            max_thick = int(sys.argv[3])
        except:
            print 'Error with thicknesses!'
            usage(action)
            sys.exit(1)

        # check for in-place option
        option = sys.argv[4]
        if option[0] is '-':
            # user input an option
            if option[1] is 'i':
                # edit rest of files in place
                for i in range(5, argc):
                    filename = sys.argv[i]
                    add_random_line(filename, filename,
                                    max_thickness=max_thick,
                                    min_thickness=min_thick)

            else:
                print 'Error: Invalid option {}'.format(option[1])
                usage(action)
                sys.exit(1)

        else:
            # no option, create new files
            for i in range(4, argc):
                filename = sys.argv[i]
                print filename
                outfile = filename.split('.')[0] + '_cropped.' \
                    + filename.split('.')[1]
                add_random_line(filename, outfile,
                                max_thickness=max_thick,
                                min_thick=min_thick)

    if action == 'crop':

        # check for appropriate usage
        if argc < 5:
            print 'Error: insufficient command line arguments!'
            usage(action)
            sys.exit(1)

        # load in height and width
        try:
            height = int(sys.argv[2])
            width = int(sys.argv[3])
        except:
            print 'Error with height/width!'
            usage(action)
            sys.exit(1)

        # check for in-place option
        option = sys.argv[4]
        if option[0] is '-':
            # user input an option
            if option[1] is 'i':
                # edit rest of files in place
                for i in range(5, argc):
                    filename = sys.argv[i]
                    autocrop(filename, filename,
                             out_height=height, out_width=width)

            else:
                print 'Error: Invalid option {}'.format(option[1])
                usage(action)
                sys.exit(1)

        else:
            # no option, create new files
            for i in range(4, argc):
                filename = sys.argv[i]
                print filename
                outfile = filename.split('.')[0] + '_cropped.' \
                    + filename.split('.')[1]
                autocrop(filename, outfile, out_height=height,
                         out_width=width)
