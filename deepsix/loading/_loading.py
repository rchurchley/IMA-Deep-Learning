from PIL import Image
import numpy as np
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


def possibly_anomalized_paths(false_values,
                              true_values,
                              switch):
    """Chooses values from two lists.

    All three arguments should be of the same length.

    Args:
        false_values (list): An arbitrary list.
        true_values (list): Another arbitrary list.
        switch (list): Decides which list to take values from false_values
            or true_values. Should consist of boolean or binary values, and
            can also be a 1d nparray.

    Return:
        A list of the same size as the parameters, where the ith element
        is either false_values[i] or true_values[i], depending on the value of
        switch[i].
    """
    result = []
    for i in range(0, len(switch)):
        if bool(switch[i]):
            result.append(true_values[i])
        else:
            result.append(false_values[i])
    return result
