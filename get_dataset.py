import deepsix.collection
from deepsix.collection import *


debug = True


if __name__ == '__main__':
    human_urls = deepsix.collection.flickr.urls_tagged(
        'person',
        max_images=40,
        apikey='Flickr_API_key.txt',
        debug=debug
    )

    # human_urls += deepsix.collection.imagenet.urls_tagged(
    #     'n07942152',
    #     max_images=5
    # )

    deepsix.collection.process_images_from_urls(human_urls, debug=debug)
