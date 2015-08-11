from PIL import ImageEnhance
import numpy


def make_white_extreme(x):
    return x/2 if x < 255 else x

make_white_extreme = numpy.vectorize(make_white_extreme)
