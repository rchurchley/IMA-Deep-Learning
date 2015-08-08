import flickrapi
# import flickrapi.shorturl as short_url
# import requests


def session(filename, debug=False):
    """Open an instance of the Flickr API given an API key."""
    if debug:
        print 'Opening FlickrAPI session!'
    api_key_file = open(filename)
    api_keys = api_key_file.readlines()
    api_key = api_keys[0].rstrip()
    api_secret = api_keys[1].rstrip()
    flickr = flickrapi.FlickrAPI(api_key, api_secret)

    return flickr


def urls_tagged(keywords, max_images, apikey, debug=False):
    """Return a list of urls of images with a given tag on Flickr."""
    flickr = session(apikey, debug=debug)
    # walk through a search query until we reach max_images
    i = 0
    image_urls = []
    for photo in flickr.walk(tag_mode='all', tags=keywords):
        if i == max_images:
            break
        if debug:
            print 'Retrieving URL {}/{}'.format(i + 1, max_images)
        photo_id = photo.get('id')
        secret = photo.get('secret')
        farm_id = photo.get('farm')
        server = photo.get('server')
        # info = flickr.photos.getInfo(photo_id=photo_id)
        # page_urls.append(short_url.url(photo_id))
        url = 'https://farm{}.staticflickr.com/{}/{}_{}.jpg'
        url = url.format(farm_id, server, photo_id, secret)
        image_urls.append(url)
        i += 1

    '''
    image_urls = []
    # parse the image urls from the website HTML
    # in case of failure, a server error has occurred, so retry the download
    for url in page_urls:
        while True:
            try:
                r = requests.get(url)
                html = r.text[:5000]
                bookend_1 = '<meta property="og:image" content="'
                bookend_2 = '"  data-dynamic="true">'
                html_buf = html.split(bookend_1)[1]
                current_url = html_buf.split(bookend_2)[0].rstrip()
                image_urls.append(current_url)
                if debug:
                    print 'Parsed URL {} from HTML'.format(current_url)
            except:
                if debug:
                    print 'Server error has occurred with URL {}!'.format(url)
                    print 'Retrying download...'
                continue
            break
    '''

    return image_urls
