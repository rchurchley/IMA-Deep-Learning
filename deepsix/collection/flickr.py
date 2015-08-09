import flickrapi
# import flickrapi.shorturl as short_url
# import requests


def session(filename):
    """Open an instance of the Flickr API given an API key."""
    with open(filename) as f:
        api_keys = f.readlines()
        api_key = api_keys[0].rstrip()
        api_secret = api_keys[1].rstrip()
        session = flickrapi.FlickrAPI(api_key, api_secret)
        return session


def urls_tagged(keywords, api_key):
    """Return a generator over images with a given tag on Flickr.

    Each element of the generator is a tuple of the form id, url.
    """
    flickr = session(api_key)
    url_template = 'https://farm{}.staticflickr.com/{}/{}_{}.jpg'
    for photo in flickr.walk(tag_mode='all', tags=keywords):
        photo_id = photo.get('id')
        secret = photo.get('secret')
        farm_id = photo.get('farm')
        server = photo.get('server')
        # info = flickr.photos.getInfo(photo_id=photo_id)
        photo_url = url_template.format(farm_id, server, photo_id, secret)
        yield photo_id, photo_url
