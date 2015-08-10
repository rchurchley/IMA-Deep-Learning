import os
import numpy


def images_in_directory(input_directory):
    """Return a dictionary of filename roots and extensions for only images.

    Extensions are not case-sensitive and include: jpg, jpeg, bmp, png.
    """
    result = {}
    for filename in os.listdir(input_directory):
        root, ext = os.path.splitext(filename)
        if ext.lower() in set(['.jpg', '.jpeg', '.bmp', '.png']):
            result[root] = ext
    return result


def list_to_array(input):
    """Return a 2d array whose rows are the elements of a list of nparrays.

    Each of the input nparrays are unraveled into a row vector.

    Args:
        input (list): A list of nparrays. The nparrays may have any shape but
            must have the same number of elements.
    """
    return numpy.vstack([numpy.ravel(a) for a in input])


def random_zero_one_array(length):
    """Return a nparray of shape (length,) with random 0-1 entries."""
    return numpy.array([numpy.random.randint(0, 2) for _ in xrange(length)])


def ensure_directory(directory_name):
    """Create a directory at a path if it does not already exist."""
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
