import flickrapi
import flickrapi.shorturl as short_url
import requests


def session(filename):
    '''
    Grab the flickr api keys from an external file. Use it to start up an
    instance of the Flickr API.
    '''
    api_key_file = open(filename)
    api_keys = api_key_file.readlines()
    api_key = api_keys[0].rstrip()
    api_secret = api_keys[1].rstrip()
    flickr = flickrapi.FlickrAPI(api_key, api_secret)

    return flickr


def urls_tagged(keywords, max_images, apikey):
    '''
    Search for images via the API based on given keywords, return a list
    of a given number of URLs for those keywords.
    '''
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
    for url in page_urls:
        r = requests.get(url)
        html = r.text
        bookend_1 = '<meta property="og:image" content="'
        bookend_2 = '"  data-dynamic="true">'
        html_buf = html.split(bookend_1)[1]
        current_url = html_buf.split(bookend_2)[0].rstrip()
        image_urls.append(current_url)

    return image_urls
