import deepsix.utils
import deepsix.loading
import numpy as np
import sys


def parallel_paths(keys, good_dict, bad_dict, good_directory, bad_directory):
    result = []
    for key in keys:
        good_path = '{}/{}{}'.format(good_directory, key, good_dict[key])
        bad_path = '{}/{}{}'.format(bad_directory, key, bad_dict[key])
        result.append((good_path, bad_path))
    return result


if __name__ == '__main__':
    if len(sys.argv) < 3:
        good_directory = 'images/64'
        bad_directory = 'images/64-random-circle'
        output_directory = 'data'
    else:
        good_directory = sys.argv[1]
        bad_directory = sys.argv[2]
        output_directory = sys.argv[3]

    good_filename_dict = deepsix.utils.image_filenames_as_dict(good_directory)
    bad_filename_dict = deepsix.utils.image_filenames_as_dict(bad_directory)
    number_of_images = len(good_filename_dict)
    train_fraction = 0.8
    validate_fraction = 0.1

    train_keys, validate_keys, test_keys = deepsix.loading.chunks_of_keys(
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
    train_data, train_labels = deepsix.loading.construct_dataset(train_candidates)
    validate_data, validate_labels = deepsix.loading.construct_dataset(validate_candidates)
    test_data, test_labels = deepsix.loading.construct_dataset(test_candidates)

    deepsix.utils.ensure_directory(output_directory)

    # Save datasets
    with open('{}/train_x.npy'.format(output_directory), 'wb') as f:
        np.save(f, train_data.astype(np.float32))
    with open('{}/train_y.npy'.format(output_directory), 'wb') as f:
        np.save(f, train_labels.astype(np.float32))
    with open('{}/val_x.npy'.format(output_directory), 'wb') as f:
        np.save(f, validate_data.astype(np.float32))
    with open('{}/val_y.npy'.format(output_directory), 'wb') as f:
        np.save(f, validate_labels.astype(np.float32))
    with open('{}/test_x.npy'.format(output_directory), 'wb') as f:
        np.save(f, test_data.astype(np.float32))
    with open('{}/test_y.npy'.format(output_directory), 'wb') as f:
        np.save(f, test_labels.astype(np.float32))
