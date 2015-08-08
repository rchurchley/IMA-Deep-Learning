from PIL import Image, ImageDraw
import numpy.random as rand
import os
from ..utils import images_in_directory


def add_random_line(filename, output_filename, min_thickness, max_thickness,
                    debug=False):
    """Add lines to an image, then save it elsewhere."""
    img = Image.open(filename)
    draw = ImageDraw.Draw(img)

    # random vertices for the rectilinear path to draw
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
                     filename_list=None,
                     min_thickness=10,
                     max_thickness=40,
                     debug=False):
    """Add lines to a subset of images in a directory and save elsewhere."""
    if not filename_list:
        filename_list = images_in_directory(input_directory)
    for filename in filename_list:
        if debug:
            print 'Adding random line to {}'.format(filename)

        add_random_line(filename=input_directory + "/" + filename,
                        output_filename=output_directory + "/" + filename,
                        min_thickness=min_thickness,
                        max_thickness=max_thickness)
