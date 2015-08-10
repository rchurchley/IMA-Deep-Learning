import deepsix.utils
import deepsix.collection
from deepsix.collection import *
import deepsix.loading
import numpy as np
import sys


def construct_dataset(good_filenames, bad_filenames):
    """Return a 2d nparray encoding images and a 1d binary array with labels.
    """
    normal_paths = ['images/28/{}'.format(s) for s in good_filenames]
    anomalized_paths = ['images/28-anomalized/{}'.format(s) for s in bad_filenames]
    anomalization = deepsix.utils.random_zero_one_array(len(normal_paths))
    paths = deepsix.loading.possibly_anomalized_paths(normal_paths,
                                                      anomalized_paths,
                                                      anomalization)
    images = deepsix.loading.load_images(paths)
    result = deepsix.utils.list_to_array(images)
    return result, anomalization


if __name__ == '__main__':
    if len(sys.argv) < 3:
        good_directory = 'images/256'
        bad_directory = 'images/256-anomalized'
        output_directory = 'data'
    else:
        good_directory = sys.argv[1]
        bad_directory = sys.argv[2]
        output_directory = sys.argv[3]

    train_fraction = 0.8
    validate_fraction = 0.1

    # Determine how many files we have downloaded, and get their filenames.
    filenames = deepsix.utils.images_in_directory(good_directory)
    bad_filenames = deepsix.utils.images_in_directory(bad_directory)
    number_of_images = len(filenames)

    # Set number of images to reserve for training and validating.
    # The remaining images will be used for testing.
    train_n = int(np.floor(train_fraction * number_of_images))
    validate_n = int(np.floor(validate_fraction * number_of_images))

    train_filenames = filenames[0:train_n]
    train_bad_filenames = bad_filenames[0:train_n]
    validate_filenames = filenames[train_n:(train_n+validate_n)]
    validate_bad_filenames = bad_filenames[train_n:(train_n+validate_n)]
    test_filenames = filenames[(train_n+validate_n):]
    test_bad_filenames = bad_filenames[(train_n+validate_n):]

    if any([len(train_filenames) == 0,
           len(validate_filenames) == 0,
           len(test_filenames) == 0]):
        raise IndexError('There are not enough files in {}.'.format(good_directory))

    # Construct datasets
    train_data, train_labels = construct_dataset(train_filenames, train_bad_filenames)
    validate_data, validate_labels = construct_dataset(validate_filenames, validate_bad_filenames)
    test_data, test_labels = construct_dataset(test_filenames, test_bad_filenames)

    # Save datasets to data/*
    with open('data/train_x.npy', 'wb') as f:
        np.save(f, train_data.astype(np.float32))
    with open('data/train_y.npy', 'wb') as f:
        np.save(f, train_labels.astype(np.float32))
    with open('data/val_x.npy', 'wb') as f:
        np.save(f, validate_data.astype(np.float32))
    with open('data/val_y.npy', 'wb') as f:
        np.save(f, validate_labels.astype(np.float32))
    with open('data/test_x.npy', 'wb') as f:
        np.save(f, test_data.astype(np.float32))
    with open('data/test_y.npy', 'wb') as f:
        np.save(f, test_labels.astype(np.float32))
