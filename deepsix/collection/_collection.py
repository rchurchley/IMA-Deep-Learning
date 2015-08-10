import requests
import shutil
import sys
import os
from ..utils import images_in_directory, ensure_directory

# Disable "Unverified HTTPS Request warnings"
requests.packages.urllib3.disable_warnings()


def get_images_from_urls(id_url_generator,
                         max_count=5,
                         output_directory='images/raw'):
    """Download JPEG images from a generator of image IDs and urls.

    Files are saved to `output_directory`, named according to their ID.

    Args:
        id_url_generator (generator): Pairs of strings (id, url).
        output_directory (str): An existing folder to save images to. Does not
            include a trailing slash.
    """
    ensure_directory(output_directory)
    already_downloaded = set(images_in_directory(output_directory))
    i = 0
    for uid, url in id_url_generator:
        i += 1
        if '{}.jpg'.format(uid) in already_downloaded:
            print '{}: Already downloaded {}'.format(i, uid)
        else:
            print '{}: Downloading {}'.format(i, url)

            try:
                response = requests.get(url, stream=True)
                if (
                    response.status_code == 200 and
                    response.headers['Content-Type'] == 'image/jpeg'
                ):
                    output_filename = '{}/{}.jpg'.format(output_directory, uid)
                    with open(output_filename, "wb") as out_file:
                        shutil.copyfileobj(response.raw, out_file)
                response.close()
            except:
                e = sys.exc_info()[0]
                print "Error: {}".format(e)

        if i >= max_count:
            break


def alter_images(procedure,
                 args,
                 input_directory,
                 output_directory,
                 output_format='JPEG'):
    """Alter all images in an input directory according to some procedure.

    Output files will be saved with the same name as the input files, but
    copied to a different directory.

    Args:
        procedure (function): One of the above functions.
        args (list): A list of arguments to pass to procedure.
        input_directory (str): A folder containing images to be altered.
        output_directory (str): An existing folder to save images to.
        output_format (str): The image format to save to, e.g. 'JPEG', 'BMP'.
    """
    filename_list = images_in_directory(input_directory)
    ensure_directory(output_directory)
    i = 0
    n = len(filename_list)
    for filename in filename_list:
        i += 1
        print '{}/{}: Applying {} to {}'.format(i, n, procedure.__name__, filename)
        input_path = '{}/{}'.format(input_directory, filename)
        root, ext = os.path.splitext(filename)
        output_path = '{}/{}.{}'.format(output_directory,
                                        root,
                                        output_format.lower())

        procedure(args,
                  path=input_path,
                  output_path=output_path,
                  output_format=output_format)
