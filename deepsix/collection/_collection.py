import requests
import shutil
import sys
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
        max_count (int): The maximum number of pictures to download. This may
            not be the same as the number of images actually downloaded, if the
            Flickr API returns duplicate images or invalid responses.
        output_directory (str): An existing folder to save images to. Does not
            include a trailing slash.
    """
    ensure_directory(output_directory)
    already_downloaded = images_in_directory(output_directory)
    i = 0
    for uid, url in id_url_generator:
        i += 1
        if uid in already_downloaded:
            print '{}: Already downloaded {}'.format(i, uid)
        else:
            print '{}: Downloading {}'.format(i, url)
            response = requests.get(url, stream=True)
            if (
                response.status_code == 200 and
                response.headers['Content-Type'] == 'image/jpeg'
            ):
                output_filename = '{}/{}.jpeg'.format(output_directory, uid)
                with open(output_filename, "wb") as out_file:
                    shutil.copyfileobj(response.raw, out_file)
            response.close()
            already_downloaded[uid] = '.jpeg'

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
        procedure (function: void): A function that saves an altered image to
            a given path. The function should have keyword arguments args,
            path, output_path, output_format. Some functions of this form
            can be found in deepsix.anomalies.
        args (list): A list of arguments to pass to procedure.
        input_directory (str): A folder containing images to be altered.
        output_directory (str): An existing folder to save images to.
        output_format (str): The image format to save to, e.g. 'JPEG', 'BMP'.
    """
    filename_dict = images_in_directory(input_directory)  # { id: extension }
    ensure_directory(output_directory)
    i = 0
    n = len(filename_dict)
    for root, ext in filename_dict.iteritems():
        i += 1
        print '{}/{}: Applying {} to {}'.format(i,
                                                n,
                                                procedure.__name__,
                                                root)

        input_path = '{}/{}{}'.format(input_directory, root, ext)
        output_path = '{}/{}.{}'.format(output_directory,
                                        root,
                                        output_format.lower())

        procedure(args=args,
                  path=input_path,
                  output_path=output_path,
                  output_format=output_format)
