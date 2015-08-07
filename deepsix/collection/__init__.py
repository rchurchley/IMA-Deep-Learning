# define subpackages loaded by `from deepsix.collection import * `
__all__ = ['flickr', 'imagenet']

# make `get_images_from_urls` available under `deepsix.collection` namespace
from downloader import get_images_from_urls
