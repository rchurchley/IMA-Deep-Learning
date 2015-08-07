import requests
import shutil
from PIL import Image
import os

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
    i = 1
    for url in urls:
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


def make_square_thumbnail(filename, output_filename, size):
    """Crop an image to a desired height and width, and save to outfile."""
    img = Image.open(filename)
    img = img.crop(box=(0, 0, min(img.size), min(img.size)))
    img.thumbnail(size=(size, size))
    img.save(output_filename)


def make_square_thumbnails(input_directory='images/raw',
                           output_directory='images/thumbnails',
                           size=200):
    for filename in os.listdir(input_directory):
        root, ext = os.path.splitext(filename)
        if ext == '.jpg' or ext == '.jpeg':
            make_square_thumbnail(input_directory + "/" + filename,
                                  output_directory + "/" + filename,
                                  size)
