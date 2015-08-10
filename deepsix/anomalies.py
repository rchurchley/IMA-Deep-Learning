from utils import images_in_directory, ensure_directory
from PIL import Image, ImageDraw
import numpy as np


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


def add_random_line(args, path, output_path, output_format):
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
    width = np.random.randint(args[0], args[1])

    color = (255, 255, 255)
    draw.line(points, fill=color, width=width)
    del draw
    img.save(output_path, output_format)


def add_circle(args, path, output_path, output_format):
    """Draw a small circle in a fixed position on an image.

    Args:
        args (None): Ignored; included only for consistency with the above.
        path (str): The file to be processed.
        output_path (str): The path to write to.
        output_format (str): The image format to save to, e.g. 'JPEG', 'BMP'.
    """
    img = Image.open(path).convert('RGB')
    draw = ImageDraw.Draw(img)
    draw.ellipse([10, 10, 15, 15], fill=(255, 255, 255))
    del draw
    img.save(output_path, output_format)
