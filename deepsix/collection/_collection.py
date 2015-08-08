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
                         filter=None,
                         debug=False):
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
    for url in urls:

        if debug:
            print 'Downloading picture from URL: {}'.format(url)
        else:
            sys.stdout.write('+')
            sys.stdout.flush()

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


def make_square_thumbnail(filename, output_filename, size, debug=False):
    """Crop the image in `filename` square, then shrink and save it."""
    if debug:
        print 'Cropping image: {}'.format(filename)
    img = Image.open(filename)
    img = img.crop(box=(0, 0, min(img.size), min(img.size)))
    img.thumbnail(size=(size, size))
    img.save(output_filename)


def make_square_thumbnails(input_directory='images/raw',
                           output_directory='images/thumbnails',
                           filename_list=None,
                           size=256,
                           debug=False):
    """Make square thumbnails for a subset of images in an input directory."""
    if not filename_list:
        filename_list = images_in_directory(input_directory)
    for filename in filename_list:
        make_square_thumbnail(filename=input_directory + "/" + filename,
                              output_filename=output_directory + "/" + filename,
                              size=size,
                              debug=debug)


def process_images_from_urls(urls, size=256, filter=None, debug=False):

    if debug:
        print 'Getting images...'
    get_images_from_urls(urls, filter=filter, debug=debug)

    if debug:
        print 'Making thumbnails...'
    make_square_thumbnails(size=size, debug=debug)

    if debug:
        print 'Adding lines...'
    anomalize.add_random_lines(debug=debug)
