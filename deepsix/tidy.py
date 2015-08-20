from utils import ensure_directory, image_filenames_as_dict
from PIL import Image
import numpy


def load_image(path, mode='L'):
    """Return a 2d nparray encoding an image after preprocessing."""
    result = numpy.array(Image.open(path).convert(mode))
    if mode == 'L':
        result = numpy.expand_dims(result, 0)
    else:
        result = numpy.swapaxes(result, 2, 0)
    result = result / 255.
    return result


def load_images(path_list, mode='L'):
    """Return a list of 2d nparrays encoding a list of images."""
    return [load_image(img, mode) for img in path_list]


def iter_image_paths(first_directory, second_directory):
    """Iterate over pairs (path, i) where path points to a file in directory i.

    Args:
        first_directory (str): The relative path to the first directory.
        second_directory (str): The relative path to the second directory.

    Yield:
        Pairs (path, i) for each file in the union of first_directory and
        second_directory. The integer i is 0 if path points to a file in
        first_directory and 1 if path points to a file in second_directory.
        If both directories contain a file with the same name, only one of the
        files is chosen (at random).
    """
    first_dictionary = image_filenames_as_dict(first_directory)
    second_dictionary = image_filenames_as_dict(second_directory)
    for key in set().union(first_dictionary, second_dictionary):
        if key in first_dictionary and key in second_dictionary:
            coinflip = numpy.random.randint(2)
        else:
            coinflip = None
        if (key not in second_dictionary) or (coinflip == 0):
            yield first_dictionary[key], 0
        else:  # (key not in first_dictionary) or (coinflip == 1):
            yield second_dictionary[key], 1


def make_dataset(first_directory, second_directory, output_directory):
    """Create and save training, validation, and test datasets.

    Datasets will be saved as numpy arrays as the files train_data.npy,
    train_labels.npy, validate_data.npy, validate_labels.npy, test_data.npy,
    and test_labels.npy in the output directory.

    Args:
        first_directory (str): The relative path to a directory of images in
            the first category the neural network should distinguish between.
        second_directory (str): The relative path to a directory of images in
            the second category the neural network should distinguish between.
        output_directory (str): The relative path to a directory for the output
            nparrays to be saved to.
    """
    pairs = list(iter_image_paths(first_directory, second_directory))
    numpy.random.shuffle(pairs)
    paths, indicators = zip(*pairs)

    n = len(paths)
    n_train = 8 * n / 10
    n_validate = 1 * n / 10
    # n_test = n - (n_train + n_validate)

    ensure_directory(output_directory)

    train_data = numpy.array(load_images(paths[:n_train]))
    train_labels = numpy.array(indicators[:n_train])

    with open('{}/train_data.npy'.format(output_directory), 'wb') as f:
        numpy.save(f, train_data.astype(numpy.float32))
    with open('{}/train_labels.npy'.format(output_directory), 'wb') as f:
        numpy.save(f, train_labels.astype(numpy.int32))

    validate_data = numpy.array(load_images(paths[n_train:n_train+n_validate]))
    validate_labels = numpy.array(indicators[n_train:n_train+n_validate])

    with open('{}/validate_data.npy'.format(output_directory), 'wb') as f:
        numpy.save(f, validate_data.astype(numpy.float32))
    with open('{}/validate_labels.npy'.format(output_directory), 'wb') as f:
        numpy.save(f, validate_labels.astype(numpy.int32))

    test_data = numpy.array(load_images(paths[n_train+n_validate:]))
    test_labels = numpy.array(indicators[n_train+n_validate:])

    with open('{}/test_data.npy'.format(output_directory), 'wb') as f:
        numpy.save(f, test_data.astype(numpy.float32))
    with open('{}/test_labels.npy'.format(output_directory), 'wb') as f:
        numpy.save(f, test_labels.astype(numpy.int32))
