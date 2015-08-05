import cv2
import numpy.random as rand


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

if __name__ == '__main__':
    picture_file = 'test.jpg'
    add_random_line(picture_file, 'test_ruined.jpg')
