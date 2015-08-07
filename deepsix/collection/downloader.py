import wget
from flickr_filtr import filterImage
import subprocess


def get_images_from_urls(image_urls, output_folder="downloads",
                         filter_type=None):
    '''
    Download a list of images from urls with wget and filter based on
    a user given filter type.
    '''
    for url in image_urls:
        filename = wget.download(url, out=output_folder)

        # filter images via a predefined filter type
        if filter_type:
            filter_result = filterImage(filename, filter_type=filter_type)
            print '{}: Filter result is {}'.format(filename, filter_result)
            # if not filter_result:
                # get rid of the file
                # subprocess.call(['rm', filename])
