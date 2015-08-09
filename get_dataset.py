import deepsix.utils
import deepsix.collection
from deepsix.collection import *
import deepsix.loading
import numpy as np


def construct_dataset(filenames):
    """Return a 2d nparray encoding images and a 1d binary array with labels.
    """
    normal_paths = ['images/thumbnails/' + s for s in filenames]
    anomalized_paths = ['images/anomalized/' + s for s in filenames]
    anomalization = deepsix.utils.random_zero_one_array(len(filenames))
    paths = deepsix.loading.possibly_anomalized_paths(normal_paths,
                                                      anomalized_paths,
                                                      anomalization)
    images = deepsix.loading.load_images(paths)
    result = deepsix.utils.list_to_array(images)
    return result, anomalization


def save_datasets(train_fraction, validate_fraction):
    # Determine how many files we have downloaded, and get their filenames.
    filenames = deepsix.utils.images_in_directory('images/thumbnails')
    number_of_images = len(filenames)

    # Set number of images to reserve for training and validating.
    # The remaining images will be used for testing.
    train_n = int(np.floor(train_fraction * number_of_images))
    validate_n = int(np.floor(validate_fraction * number_of_images))

    train_filenames = filenames[0:train_n]
    validate_filenames = filenames[train_n:(train_n+validate_n)]
    test_filenames = filenames[(train_n+validate_n):]

    if any([len(train_filenames) == 0,
           len(validate_filenames) == 0,
           len(test_filenames) == 0]):
        raise IndexError('There are not enough files in images/thumbnails.')

    # Construct datasets
    train_data, train_labels = construct_dataset(train_filenames)
    validate_data, validate_labels = construct_dataset(validate_filenames)
    test_data, test_labels = construct_dataset(test_filenames)

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


if __name__ == '__main__':

    # Get a list of URLs of images to download.
    human_urls = deepsix.collection.flickr.urls_tagged(
        'person',
        api_key='Flickr_API_key.txt')

    # Download images, crop and resize them, and generate 'bad' copies.
    deepsix.collection.get_images_from_urls(human_urls, max_count=10)
    deepsix.collection.make_small_squares(size=256)
    deepsix.collection.anomalize.add_random_lines()

    # Construct training, validation, and test datasets and save them.
    save_datasets(train_fraction=0.8, validate_fraction=0.1)
