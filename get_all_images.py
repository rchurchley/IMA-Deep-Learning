"""
Required packages
- flickrapi
- requests
- wget
"""

import deepsix.flickr
import deepsix.imagenet
import deepsix.download

if __name__ == '__main__':
    flickr = deepsix.flickr.session('Flickr_API_key.txt')
    human_urls = deepsix.flickr.urls_with_keywords(flickr, 'human', 4)
    human_urls += deepsix.imagenet.urls_with_synset('n07942152', 5)
    deepsix.download.get_images_from_urls(human_urls, output_folder='downloads')
