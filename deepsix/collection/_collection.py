import requests
import shutil
import os
import sys
from PIL import Image
from . import anomalize
from ..utils import images_in_directory

# Disable "Unverified HTTPS Request warnings"
requests.packages.urllib3.disable_warnings()


def get_images_from_urls(urls,
                         output_directory='images/raw',
                         filter=None):
    """Download JPEG images from a list of urls.

    Files are saved with consecutively numbered names to `output_directory`.

    Keyword arguments:
    urls             -- a list of urls.
    output_directory -- an existing folder (no trailing slash) for images.
    filter           -- a function taking an Image and returning a boolean.
                        Images returning False will not be saved.
    """
    print "Downloading images..."
    i = 1
    n = len(urls)
    for url in urls:
        print 'Downloading {}/{} from {}'.format(i, n, url)

        response = requests.get(url, stream=True)
        if (
            response.status_code == 200 and
            response.headers['Content-Type'] == 'image/jpeg'
        ):
            if filter:
                # TODO
                # load image (e.g. with requests and StringIO)
                # if filter(image) == True, save it.
                pass
            else:
                output_filename = output_directory + "/" + str(i) + ".jpg"
                with open(output_filename, "wb") as out_file:
                    shutil.copyfileobj(response.raw, out_file)
        response.close()
        i += 1


def make_small_square(filename, output_filename, size):
    """Crop the image in `filename` square, then shrink and save it."""
    img = Image.open(filename)
    img = img.crop(box=(0, 0, min(img.size), min(img.size)))
    img = img.resize(size=(size, size))
    img.save(output_filename)


def make_small_squares(input_directory='images/raw',
                       output_directory='images/thumbnails',
                       filename_list=None,
                       size=256):
    """Make square thumbnails for a subset of images in an input directory."""
    if not filename_list:
        filename_list = images_in_directory(input_directory)
    for filename in filename_list:
        print 'Resizing {}'.format(filename)
        make_small_square(filename=input_directory + "/" + filename,
                          output_filename=output_directory + "/" + filename,
                          size=size)
