import deepsix.loading
from deepsix.loading import *
import sys


if __name__ == '__main__':
    if len(sys.argv) < 3:
        good_directory = 'images/64'
        bad_directory = 'images/64-random-rectangle'
        output_directory = 'data/test'
    else:
        good_directory = sys.argv[1]
        bad_directory = sys.argv[2]
        output_directory = sys.argv[3]

    deepsix.loading.make_and_save_dataset(
        good_directory,
        bad_directory,
        output_directory,
        deepsix.loading.preprocessors.posterize3)
