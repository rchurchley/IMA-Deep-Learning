import requests
import shutil
import os
import sys
from PIL import Image
from . import anomalize

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
                           size=200,
                           debug=False):
    """Make square thumbnails for all images in `input_directory`."""
    for filename in os.listdir(input_directory):
        root, ext = os.path.splitext(filename)
        if ext == '.jpg' or ext == '.jpeg':
            make_square_thumbnail(input_directory + "/" + filename,
                                  output_directory + "/" + filename,
                                  size, debug=debug)


def process_images_from_urls(urls, filter=None, debug=False):

    if debug:
        print '\n---------------\nGetting images!\n---------------\n'
    get_images_from_urls(urls, filter=filter, debug=debug)

    if debug:
        print '\n------------------\nMaking thumbnails!\n------------------\n'
    make_square_thumbnails(debug=debug)

    if debug:
        print '\n-------------\nAdding lines!\n-------------\n'
    anomalize.add_random_lines(debug=debug)
