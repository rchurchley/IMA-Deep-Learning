import cv2
import sys


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


def usage(action):
    '''
    Print usage for a specific action keyword.
    '''
    print 'Usage:'
    if action == 'crop':
        print 'python pic_tools.py action [height] [width] ' \
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
