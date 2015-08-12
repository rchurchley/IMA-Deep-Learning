import os
import numpy


def image_filenames_as_dict(input_directory):
    """Return a dictionary of filename roots and extensions for only images.

    Extensions are not case-sensitive and include: jpg, jpeg, bmp, png.
    """
    result = {}
    for filename in os.listdir(input_directory):
        root, ext = os.path.splitext(filename)
        if ext.lower() in set(['.jpg', '.jpeg', '.bmp', '.png']):
            result[root] = ext
    return result


def ensure_directory(directory_name):
    """Create a directory at a path if it does not already exist."""
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
