import deepsix.collection
from deepsix.collection import *
import sys
import os

if __name__ == '__main__':
    if len(sys.argv) == 1:
        size = 256
    else:
        size = sys.argv[1]

    thumbnail_directory = 'images/{}'.format(size)
    anomalized_directory = 'images/{}-anomalized'.format(size)

    if not os.path.exists(thumbnail_directory):
        os.makedirs(thumbnail_directory)

    if not os.path.exists(anomalized_directory):
        os.makedirs(anomalized_directory)

    deepsix.collection.make_small_squares(
        size=size,
        output_directory=thumbnail_directory
    )

    deepsix.collection.anomalize.add_random_lines(
        input_directory=thumbnail_directory,
        output_directory=anomalized_directory
    )
