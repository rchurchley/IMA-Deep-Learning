from PIL import Image
import numpy
# import cv2

from ..utils import random_zero_one_array, list_to_array


def load_image(path):
    """Return a 2d nparray encoding an image.

    Each entry of the array is an integer from 0 to 255 encoding the greyscale
    value of a pixel.
    """
    return numpy.array(Image.open(path).convert('L'))
    # return cv2.imread(path, 0)  # twice as fast but not always available


def load_images(path_list):
    """Return a list of 2d nparrays encoding a list of images."""
    return [load_image(img) for img in path_list]


def possibly_anomalized_paths(value_pairs,
                              switch):
    """Chooses values from two lists.

    All three arguments should be of the same length.

    Args:
        value_pairs (list): A list of pairs of strings.
        switch (list): A list (or 1d nparray) with 0/1 values.

    Return:
        A list of size len(value_pairs) where the ith element is one of the
        two elements stored in value_pairs[i], depending on the value of
        switch[i].
    """
    return [value_pairs[i][int(switch[i])] for i in range(0, len(switch))]


def construct_dataset(path_pairs):
    """Randomly choose good and bad datapoints and return the nparrays.

    Args:
        path_pairs (list (str, str)): A list of pairs each containing the path
            of a 'good' image and a corresponding 'bad' image.

    Return:
        A tuple result, labels. The 2d nparray `result` contains in row i the
        data of the image at either the good or bad path. The 1d nparray
        `labels` contains 0 in the ith position in the former case and 1 in the
        ith position in the latter.
    """
    labels = random_zero_one_array(len(path_pairs))
    paths = possibly_anomalized_paths(path_pairs, labels)
    images = load_images(paths)
    result = list_to_array(images)
    return result, labels
