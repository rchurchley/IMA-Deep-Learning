from utils import ensure_directory
from PIL import Image, ImageDraw
import numpy


def resize(args, path, output_path, output_format):
    """Crop an image to square aspect ratio, then resize it.

    Args:
        args (int): The square side length to resize to.
        path (str): The file to be processed.
        output_path (str): The path to write to.
        output_format (str): The image format to save to, e.g. 'JPEG', 'BMP'.
    """
    size = args
    img = Image.open(path)
    img = img.resize(size=(size, size))
    img.save(output_path, output_format)


def add_line(args, path, output_path, output_format):
    """Scribble over an image with a random white line, saving to another file.

    Args:
        args (list): A list containing the min and max brush thickness to use.
        path (str): The file to be processed.
        output_path (str): The path to write to.
        output_format (str): The image format to save to, e.g. 'JPEG', 'BMP'.
    """
    img = Image.open(path).convert('RGB')
    draw = ImageDraw.Draw(img)

    points = []
    for _ in xrange(4):
        # This assumes that the height and width of the image are equal.
        points.append(numpy.random.randint(0, img.size[0]))
    width = numpy.random.randint(args[0], args[1])

    color = (255, 255, 255)
    draw.line(points, fill=color, width=width)
    del draw
    img.save(output_path, output_format)


def add_rectangle(args, path, output_path, output_format):
    """Draw a rectangle in a given or random position on an image.

    Args:
        args (int or list): A list containing the left, top, right, and bottom
            of the rectangle, or an integer containing the side length of a
            square to be positioned randomly.
        path (str): The file to be processed.
        output_path (str): The path to write to.
        output_format (str): The image format to save to, e.g. 'JPEG', 'BMP'.
    """
    img = Image.open(path).convert('RGB')
    draw = ImageDraw.Draw(img)

    if isinstance(args, list):
        bounding_box = args
    else:
        size = args
        x = numpy.random.randint(0, img.size[0] - size)
        y = numpy.random.randint(0, img.size[1] - size)
        bounding_box = [x, y, x + size, y + size]
    draw.rectangle(bounding_box, fill=(255, 255, 255))
    del draw
    img.save(output_path, output_format)
