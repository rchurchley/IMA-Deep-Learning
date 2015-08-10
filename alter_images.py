import deepsix.collection
from deepsix.collection import *
from deepsix.utils import ensure_directory
import sys
import os

if __name__ == '__main__':
    if len(sys.argv) == 1:
        size = 28
    else:
        size = int(sys.argv[1])

    thumbnail_directory = 'images/{}'.format(size)
    anomalized_directory = 'images/{}-anomalized'.format(size)

    ensure_directory(thumbnail_directory)
    ensure_directory(anomalized_directory)

    # deepsix.collection.make_small_squares(
    #    size=size,
    #    output_directory=thumbnail_directory
    #)

    deepsix.collection.anomalize.add_circles(
        input_directory=thumbnail_directory,
        output_directory=anomalized_directory
    )
