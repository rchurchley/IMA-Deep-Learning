from PIL import Image, ImageDraw
import numpy.random as rand
import os


def add_random_line(filename, output_filename, min_thickness, max_thickness,
                    debug=False):
    img = Image.open(filename)
    draw = ImageDraw.Draw(img)
    # define random vertices for the rectilinear path to draw
    points = [
        (rand.randint(0, img.size[0]), rand.randint(0, img.size[1])),
        (rand.randint(0, img.size[0]), rand.randint(0, img.size[1]))
    ]
    color = (255, 255, 255)
    width = rand.randint(min_thickness, max_thickness)
    draw.line(points, fill=color, width=width)
    del draw

    img.save(output_filename, "JPEG")


def add_random_lines(input_directory='images/thumbnails',
                     output_directory='images/anomalized',
                     min_thickness=10,
                     max_thickness=40,
                     debug=False):
    for filename in os.listdir(input_directory):
        root, ext = os.path.splitext(filename)
        if ext == '.jpg' or ext == '.jpeg':
            if debug:
                print 'Adding random line to {}'.format(filename)

            add_random_line(input_directory + "/" + filename,
                            output_directory + "/" + filename,
                            min_thickness,
                            max_thickness)
