import deepsix.collection
from deepsix.collection import *
import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        count = 10
    else:
        count = sys.argv[1]

    # Get a list of URLs of images to download.
    human_urls = deepsix.collection.flickr.urls_tagged(
        'person',
        api_key='Flickr_API_key.txt')

    deepsix.collection.get_images_from_urls(human_urls,
                                            max_count=count,
                                            output_directory='images/raw')
