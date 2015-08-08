import os


def images_in_directory(input_directory):
    """Return a list of filenames in `input_directory` with JPEG extension.

    As with os.listdir, output filenames are not prefixed with their directory.
    """
    result = []
    for filename in os.listdir(input_directory):
        root, ext = os.path.splitext(filename)
        if ext == '.jpg' or ext == '.jpeg':
            result.append(filename)
    return result
