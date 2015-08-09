import requests
import shutil
import sys
from PIL import Image
from ..utils import images_in_directory

# Disable "Unverified HTTPS Request warnings"
requests.packages.urllib3.disable_warnings()


def get_images_from_urls(id_url_generator,
                         max_count=5,
                         output_directory='images/raw',
                         filter=None):
    """Download JPEG images from a generator of image IDs and urls.

    Files are saved to `output_directory`, named according to their ID.

    Keyword arguments:
    id_url_generator -- a generator yielding pairs of strings (id, url).
    output_directory -- an existing folder, no trailing slash, for images.
    filter           -- a function taking an Image and returning a boolean.
                        Images returning False will not be saved.
    """
    i = 0
    for uid, url in id_url_generator:
        i += 1
        print '{}: Downloading {}'.format(i, url)

        try:
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
                    output_filename = '{}/{}.jpg'.format(output_directory, uid)
                    with open(output_filename, "wb") as out_file:
                        shutil.copyfileobj(response.raw, out_file)
            response.close()
        except:
            e = sys.exc_info()[0]
            print "Error: {}".format(e)
        if i >= max_count:
            break


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
    i = 0
    n = len(filename_list)
    for filename in filename_list:
        i += 1
        print '{}/{}: Resizing {}'.format(i, n, filename)
        make_small_square(filename=input_directory + "/" + filename,
                          output_filename=output_directory + "/" + filename,
                          size=size)
