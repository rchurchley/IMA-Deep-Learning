import deepsix.collection
from deepsix.collection import *
import sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        keywords = 'nikon'
        count = 20
    else:
        keywords = sys.argv[1]
        count = int(sys.argv[2])

    # Get a list of URLs of images to download.
    urls = deepsix.collection.flickr.urls_tagged(
        keywords,
        api_key='Flickr_API_key.txt')

    deepsix.collection.get_images_from_urls(urls,
                                            max_count=count,
                                            output_directory='images/raw')
