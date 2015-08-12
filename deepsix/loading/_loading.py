from PIL import Image
import numpy
# import cv2

from ..utils import ensure_directory, image_filenames_as_dict


def identity(input):
    return input


def load_image(path, preprocessor=identity, mode='L'):
    """Return a 2d nparray encoding an image after preprocessing."""
    return preprocessor(numpy.array(Image.open(path).convert(mode)))
    # return cv2.imread(path, 0)  # twice as fast but not always available


def load_images(path_list, preprocessor=identity, mode='L'):
    """Return a list of 2d nparrays encoding a list of images."""
    return [load_image(img, preprocessor, mode) for img in path_list]


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


def chunks_of_keys(input_dict, proportions):
    """Return a partition of the keys of an input dictionary.

    Args:
        input_dict (dict): An arbitrary dictionary.
        proportions (list): A list of k floats whose sum is less than one,
            representing the fraction of input_dict each output should cover.

    Return:
        A tuple of k + 1 dictionaries which partition the input dictionary.
        The size of the first k dictionaries is determined by proportions;
        the last dictionary contains the remaining key-value pairs.
    """
    result = ()
    temp_set = set()
    i = 0  # counts items that have been processed
    j = 0  # counts output dictionaries that have been finished
    k = len(proportions)
    total_keys = len(input_dict)

    def next_checkpoint(l, j, n):
        return int(numpy.floor(sum(l[:j+1]) * n))

    checkpoint = next_checkpoint(proportions, j, total_keys)
    for key in input_dict:
        temp_set.add(key)
        i += 1
        if i >= checkpoint:
            # We have filled the jth dictionary. Add the dictionary to the
            # tuple and clear it. If j = k, we set checkpoint = total_keys
            # to fill the last dictionary with all remaining keys.
            j += 1
            result += (temp_set.copy(),)
            temp_set.clear()
            if j < k:
                checkpoint = next_checkpoint(proportions, j, total_keys)
            else:
                checkpoint = total_keys
    return result


def construct_dataset(path_pairs, preprocessor=identity, mode='L'):
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
    images = load_images(paths, preprocessor, mode)
    result = list_to_array(images)
    return result, labels


def parallel_paths(keys, good_dict, bad_dict, good_directory, bad_directory):
    result = []
    for key in keys:
        good_path = '{}/{}{}'.format(good_directory, key, good_dict[key])
        bad_path = '{}/{}{}'.format(bad_directory, key, bad_dict[key])
        result.append((good_path, bad_path))
    return result


def make_and_save_dataset(good_directory,
                          bad_directory,
                          output_directory,
                          preprocessor):
    good_filename_dict = image_filenames_as_dict(good_directory)
    bad_filename_dict = image_filenames_as_dict(bad_directory)
    number_of_images = len(good_filename_dict)
    train_fraction = 0.8
    validate_fraction = 0.1

    train_keys, validate_keys, test_keys = chunks_of_keys(
        good_filename_dict,
        [train_fraction,
         validate_fraction])

    train_candidates = parallel_paths(train_keys,
                                      good_filename_dict,
                                      bad_filename_dict,
                                      good_directory,
                                      bad_directory)
    validate_candidates = parallel_paths(validate_keys,
                                         good_filename_dict,
                                         bad_filename_dict,
                                         good_directory,
                                         bad_directory)
    test_candidates = parallel_paths(test_keys,
                                     good_filename_dict,
                                     bad_filename_dict,
                                     good_directory,
                                     bad_directory)

    if any([len(train_candidates) == 0,
           len(validate_candidates) == 0,
           len(test_candidates) == 0]):
        raise IndexError('There are not enough files in {}.'.format(good_directory))

    # Construct datasets
    train_data, train_labels = construct_dataset(
        train_candidates,
        preprocessor=preprocessor)
    validate_data, validate_labels = construct_dataset(
        validate_candidates,
        preprocessor=preprocessor)
    test_data, test_labels = construct_dataset(
        test_candidates,
        preprocessor=preprocessor)

    ensure_directory(output_directory)

    # Save datasets
    with open('{}/train_x.npy'.format(output_directory), 'wb') as f:
        numpy.save(f, train_data.astype(numpy.float32))
    with open('{}/train_y.npy'.format(output_directory), 'wb') as f:
        numpy.save(f, train_labels.astype(numpy.float32))
    with open('{}/val_x.npy'.format(output_directory), 'wb') as f:
        numpy.save(f, validate_data.astype(numpy.float32))
    with open('{}/val_y.npy'.format(output_directory), 'wb') as f:
        numpy.save(f, validate_labels.astype(numpy.float32))
    with open('{}/test_x.npy'.format(output_directory), 'wb') as f:
        numpy.save(f, test_data.astype(numpy.float32))
    with open('{}/test_y.npy'.format(output_directory), 'wb') as f:
        numpy.save(f, test_labels.astype(numpy.float32))
