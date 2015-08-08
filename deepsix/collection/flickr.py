import flickrapi
import flickrapi.shorturl as short_url
import requests


def session(filename):
    """Open an instance of the Flickr API given an API key."""
    api_key_file = open(filename)
    api_keys = api_key_file.readlines()
    api_key = api_keys[0].rstrip()
    api_secret = api_keys[1].rstrip()
    flickr = flickrapi.FlickrAPI(api_key, api_secret)

    return flickr


def urls_tagged(keywords, max_images, apikey):
    """Return a list of urls of images with a given tag on Flickr."""
    flickr = session(apikey)
    # walk through a search query until we reach max_images
    i = 0
    page_urls = []
    for photo in flickr.walk(tag_mode='all', tags=keywords):
        if i == max_images:
            break
        photo_id = photo.get('id')
        page_urls.append(short_url.url(photo_id))
        i += 1

    image_urls = []
    # parse the image urls from the website HTML
    # in case of failure, a server error has occurred, so retry the download
    for url in page_urls:
        while True:
            try:
                r = requests.get(url)
                html = r.text
                bookend_1 = '<meta property="og:image" content="'
                bookend_2 = '"  data-dynamic="true">'
                html_buf = html.split(bookend_1)[1]
                current_url = html_buf.split(bookend_2)[0].rstrip()
                image_urls.append(current_url)
            except:
                print 'A server error has occurred! Retrying download...'
                continue
            break

    return image_urls
