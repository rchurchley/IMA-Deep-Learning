import os
import numpy as np
import PIL
from PIL import Image
from PIL import ImageDraw

def images_in_directory(input_directory):
    """Return a list of filenames in `input_directory` with JPEG extension.

    As with os.listdir, output filenames are not prefixed with their directory.
    """
    result = []
    for filename in os.listdir(input_directory):
        root, ext = os.path.splitext(filename)
        if ext == '.jpg' or ext == '.jpeg' or ext == '.bmp':
            result.append(filename)
    return result

number_of_images = 50000

for i in range(1,number_of_images+1):
    #make the bitmap then call the functions from deepsix
    Im = Image.new('L',[28,28],color=0)
    Im.save('primitive/thumbnails/' +  str(i) + '.bmp' , 'BMP' )

files = images_in_directory('primitive/thumbnails/')

for file in files:
    #draw on them

    Im = Image.open('primitive/thumbnails/'+file)
    draw = ImageDraw.Draw(Im)
    draw.ellipse([8,8,20,20],fill='white')
    Im.save('primitive/anomalized/' +  str(file) + '.bmp' , 'BMP' )

