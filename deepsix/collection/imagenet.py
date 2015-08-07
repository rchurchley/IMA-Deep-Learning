import requests

def urls_tagged(category_id, max_images=None):
	'''Get the urls of up to max_count images from ImageNet from the given category.'''
	r = requests.get('http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=' + category_id)
	urls = [l.encode('ascii', 'ignore') for l in r.text.splitlines(True)]
	if max_images:
		return urls[0:max_images]
	else:
		return urls
