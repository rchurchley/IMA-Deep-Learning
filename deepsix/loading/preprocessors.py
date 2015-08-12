from PIL import ImageEnhance
import numpy
import scipy

def make_binary(x):
    return 255 if x == 255 else 0


def make_white_extreme(x):
    return x/2 if x < 255 else x

make_binary = numpy.vectorize(make_binary)
make_white_extreme = numpy.vectorize(make_white_extreme)

def sobel(x)
    #should be applied to images before they are raveled.
    #sobel_x = np.array([[-1,0,1],[-2,0,2],[-1,0,1]]).astype(float32)
    #sobel_y = np.array([[-1,-2,-1],[0,0,0],[1,2,1]]).astype(float32)
    scipy.ndimage.filters.sobel(x,axis=-1,output=y,mode='reflect')
    return y

def med_filter(x)
    #should be applied to images before they are raveled
    scipy.ndimage.filters.median_filter(input, size=2, output=y, mode='reflect', cval=0.0, origin=0)
    return y
    