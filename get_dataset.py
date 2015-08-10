import deepsix.utils
import deepsix.collection
from deepsix.collection import *
import deepsix.loading
import numpy as np
import sys


if __name__ == '__main__':
    if len(sys.argv) < 3:
        good_directory = 'images/28'
        bad_directory = 'images/28-anomalized'
        output_directory = 'data'
    else:
        good_directory = sys.argv[1]
        bad_directory = sys.argv[2]
        output_directory = sys.argv[3]

    train_fraction = 0.8
    validate_fraction = 0.1

    # filename_dict = { id: extension }
    good_filename_dict = deepsix.utils.images_in_directory(good_directory)
    bad_filename_dict = deepsix.utils.images_in_directory(bad_directory)
    number_of_images = len(good_filename_dict)

    # Set number of images to reserve for training and validating.
    # The remaining images will be used for testing.
    train_n = int(np.floor(train_fraction * number_of_images))
    validate_n = int(np.floor(validate_fraction * number_of_images))

    train_candidates = []
    validate_candidates = []
    test_candidates = []

    i = 0
    for root, ext in good_filename_dict.iteritems():
        candidate_pair = (good_directory + '/' + root + ext, bad_directory + '/' + root + bad_filename_dict[root])
        if i < train_n:
            train_candidates.append(candidate_pair)
        elif i < train_n + validate_n:
            validate_candidates.append(candidate_pair)
        else:
            test_candidates.append(candidate_pair)
        i += 1

    if any([len(train_candidates) == 0,
           len(validate_candidates) == 0,
           len(test_candidates) == 0]):
        raise IndexError('There are not enough files in {}.'.format(good_directory))

    # Construct datasets
    train_data, train_labels = deepsix.loading.construct_dataset(train_candidates)
    validate_data, validate_labels = deepsix.loading.construct_dataset(validate_candidates)
    test_data, test_labels = deepsix.loading.construct_dataset(test_candidates)

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
