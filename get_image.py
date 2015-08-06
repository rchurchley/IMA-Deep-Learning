#! /usr/bin/python

import requests
import subprocess
import sys

def get_image_urls(category_id='n07942152', max_count=None, output_file='image_urls.txt'):
	'''Get the urls of up to max_count images from ImageNet from the given category.'''
	r = requests.get('http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=' + category_id)
	urls = [l.encode('ascii', 'ignore') for l in r.text.splitlines(True)]
	with open(output_file, 'wb') as f:
		if max_count:
			f.writelines(urls[0:max_count])
		else:
			f.writelines(urls)

def get_images(filename='image_urls.txt', output_directory='downloads'):
	subprocess.call(['wget', '--quiet', '--show-progress', '-i', filename, '-P', output_directory])

if __name__ == '__main__':
	if len(sys.argv) > 1:
		get_image_urls(max_count=int(sys.argv[1]))
	else:
		get_image_urls(max_count=20)
	get_images()
