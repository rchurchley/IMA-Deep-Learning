from ..utils import images_in_directory, ensure_directory
from PIL import Image, ImageDraw
import numpy as np


def add_random_line(filename, output_filename, min_thickness, max_thickness):
    """Add lines to an image, then save it to output_filename."""

    # Ensure
    img = Image.open(filename).convert('RGB')
    draw = ImageDraw.Draw(img)
    points = [
        (np.random.randint(0, img.size[0]), np.random.randint(0, img.size[1])),
        (np.random.randint(0, img.size[0]), np.random.randint(0, img.size[1]))
    ]
    color = (255, 255, 255)
    width = np.random.randint(min_thickness, max_thickness)
    draw.line(points, fill=color, width=width)
    del draw

    img.save(output_filename, "JPEG")


def add_random_lines(input_directory='images/thumbnails',
                     output_directory='images/anomalized',
                     filename_list=None,
                     min_thickness=10,
                     max_thickness=40):
    """Scribble over a subset of images in an input directory.

    Output files will be saved with the same name as the input files, but
    copied to a different directory.

    Args:
        input_directory (str): A folder containing images to be altered.
        output_directory (str): An existing folder to save images to.
        filename_list (list(str)): A list of filenames from input_directory to
            be altered. Filenames are not full paths and should not include the
            prefix input_directory. If no list is provided, all images in
            input_directory will be processed.
        min_thickness (int): The minimum brush thickness for the scribbles.
        max_thickness (int): The maximum brush thickness for the scribbles.
    """
    if not filename_list:
        filename_list = images_in_directory(input_directory)
    ensure_directory(output_directory)
    i = 0
    n = len(filename_list)
    for filename in filename_list:
        i += 1
        print '{}/{}: Scribbling over {}'.format(i, n, filename)

        add_random_line(filename=input_directory + "/" + filename,
                        output_filename=output_directory + "/" + filename,
                        min_thickness=min_thickness,
                        max_thickness=max_thickness)
