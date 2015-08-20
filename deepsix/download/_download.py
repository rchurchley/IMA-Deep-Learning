import requests
import shutil
from ..utils import image_filenames_as_dict, ensure_directory

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
    already_downloaded = image_filenames_as_dict(output_directory)
    i = 1
    with requests.Session() as s:
        for uid, url in id_url_generator:
            if uid in already_downloaded:
                print '{}: Already downloaded {}'.format(i, uid)
            else:
                print '{}: Downloading {}'.format(i, url)
                response = s.get(url, stream=True)
                if (
                    response.status_code == 200 and
                    response.headers['Content-Type'] == 'image/jpeg'
                ):
                    filename = '{}/{}.jpeg'.format(output_directory, uid)
                    with open(filename, "wb") as out_file:
                        shutil.copyfileobj(response.raw, out_file)
                        already_downloaded[uid] = filename
            if i < max_count:
                i += 1
            else:
                break
