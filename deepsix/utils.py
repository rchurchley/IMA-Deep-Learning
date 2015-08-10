import os
import numpy as np


def images_in_directory(input_directory):
    """Return a list of filenames in `input_directory` with JPEG extension.

    As with os.listdir, output filenames are not prefixed with their directory.
    """
    result = []
    for filename in os.listdir(input_directory):
        root, ext = os.path.splitext(filename)
        if ext.lower() in set(['.jpg', '.jpeg', '.bmp']):
            result.append(filename)
    return result


def random_zero_one_array(length):
    """Return a nparray of shape (length,) with random 0-1 entries."""
    return np.array([np.random.randint(0, 2) for _ in xrange(length)])


def list_to_array(input):
    """Return a 2D array whose rows are the elements of a list of nparrays.

    Each of the input nparrays are unraveled into a row vector.
    All of the nparrays must have the same number of entries.
    """
    return np.vstack([np.ravel(a) for a in input])


def ensure_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
