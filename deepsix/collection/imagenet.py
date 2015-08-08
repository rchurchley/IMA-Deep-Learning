import requests


def urls_tagged(category_id, max_images=None, debug=False):
    """Return a list of urls of images from a given synset in ImageNet."""
    r = requests.get(
        'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=' +
        category_id
    )

    if debug:
        print 'Requesting ImageNet URLs for Synset: {}'.format(category_id)

    urls = [l.encode('ascii', 'ignore') for l in r.text.splitlines()]

    if max_images:
        return urls[0:max_images]
    else:
        return urls
