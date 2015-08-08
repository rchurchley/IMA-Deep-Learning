import os
import deepsix.utils
import deepsix.loading as d6l


def construct_dataset(filenames):
    """Return a 2d nparray encoding images and a 1d binary array with labels.
    """
    normal_paths = ['images/thumbnails/' + s for s in filenames]
    anomalized_paths = ['images/anomalized/' + s for s in filenames]
    anomalization = deepsix.utils.random_zero_one_array(len(filenames))
    paths = d6l.possibly_anomalized_paths(normal_paths,
                                          anomalized_paths,
                                          anomalization)
    images = d6l.load_images(paths)
    result = deepsix.utils.list_to_array(images)
    return result, anomalization


filenames = deepsix.utils.images_in_directory('images/thumbnails')
number_of_images = len(filenames)

# Define number of images to reserve for training and validating.
# The remaining images will be used for testing.
train_n = 8 * number_of_images / 10  # integer division
validate_n = 1 * number_of_images / 10

train_filenames = filenames[0:train_n]
validate_filenames = filenames[train_n:(train_n+validate_n)]
test_filenames = filenames[(train_n+validate_n):]

train_data, train_labels = construct_dataset(train_filenames)
validate_data, validate_labels = construct_dataset(validate_filenames)
test_data, test_labels = construct_dataset(test_filenames)
