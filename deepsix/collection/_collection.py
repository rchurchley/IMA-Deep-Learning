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

    Args:
        id_url_generator (generator): Pairs of strings (id, url).
        output_directory (str): An existing folder to save images to. Does not
            include a trailing slash.
        filter (function: Image -> bool): Decides which images to process.
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
    """Crop an image to square aspect ratio, then resize it to (size, size)."""
    img = Image.open(filename)
    img = img.crop(box=(0, 0, min(img.size), min(img.size)))
    img = img.resize(size=(size, size))
    img.save(output_filename)


def make_small_squares(input_directory='images/raw',
                       output_directory='images/thumbnails',
                       filename_list=None,
                       size=256):
    """Make square thumbnails for a subset of images in an input directory.

    Output files will be saved with the same name as the input files, but
    copied to a different directory.

    Args:
        input_directory (str): A folder containing images to be resized.
        output_directory (str): An existing folder to save images to.
        filename_list (list(str)): A list of filenames from input_directory to
            be resized. Filenames are not full paths and should not include the
            prefix input_directory. If no list is provided, all images in
            input_directory will be processed.
        size (int): The side length of the square image to be saved.
    """
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
