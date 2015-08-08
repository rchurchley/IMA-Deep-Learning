import numpy as np
from PIL import Image
# import cv2

from ..utils import images_in_directory


def load_image(filename):
    """Return a 2d nparray encoding an image.

    Each entry of the array is an integer from 0 to 255 encoding the greyscale
    value of a pixel.
    """
    return np.array(Image.open(filename).convert('L'))
    # return cv2.imread(filename, 0)  # twice as fast but not always available


def load_images(filename_list):
    """Return a list of 2d nparrays encoding a list of images."""
    return [load_image(img) for img in filename_list]


def possibly_anomalized_paths(normal_paths,
                              anomalized_paths,
                              anomalization):
    """Return a list of paths, each coming from one of two lists.

    The ith element of the resulting list of paths is either normal_paths[i] or
    anomalized_paths[i], depending on the value of anormalization[i].
    All three arguments should be of the same length.

    Keyword arguments:
    normal_paths     -- a list of 'normal' paths
    anomalized_paths -- a list of corresponding anomalized paths
    anomalization    -- a list or vector of 0-1 or boolean values encoding
                        whether to return the normal or anomalized version of
                        each path.
    """
    result = []
    for i in range(0, len(anomalization)):
        if bool(anomalization[i]):
            result.append(anomalized_paths[i])
        else:
            result.append(normal_paths[i])
    return result
