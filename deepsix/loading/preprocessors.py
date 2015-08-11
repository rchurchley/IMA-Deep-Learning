from PIL import ImageEnhance
import numpy


def make_binary(x):
    return 255 if x == 255 else 0


def make_white_extreme(x):
    return x/2 if x < 255 else x

make_binary = numpy.vectorize(make_binary)
make_white_extreme = numpy.vectorize(make_white_extreme)
