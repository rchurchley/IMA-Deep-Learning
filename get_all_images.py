"""
Required packages
- flickrapi
- requests
- wget
"""

import deepsix.collection
from deepsix.collection import *

if __name__ == '__main__':
    flickr = deepsix.collection.flickr.session('Flickr_API_key.txt')
    human_urls = deepsix.collection.flickr.urls_with_keywords(flickr, 'human', 4)
    human_urls += deepsix.collection.imagenet.urls_with_synset('n07942152', 5)
    deepsix.collection.get_images_from_urls(human_urls, output_folder='downloads')
