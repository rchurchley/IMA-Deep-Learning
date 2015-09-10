import deepsix
from deepsix import *
from deepsix.download import *
from deepsix.tidy import make_dataset
from deepsix.utils import ensure_directory, alter_images
import IPython
from PIL import Image
from numpy.random import randint


def create(number):
    ensure_directory('images/black')
    for i in range(1, number + 1):
        Im = Image.new('L', [64, 64], color=0)
        Im.save('images/black/{}.bmp'.format(i), 'BMP')


def create_colours(number):
    ensure_directory('images/solid')
    for i in range(1, number + 1):
        random = (randint(255), randint(255), randint(255))
        Im = Image.new('RGB', [64, 64], color=random)
        Im.save('images/solid/{}.bmp'.format(i), 'BMP')


def download_flickr(keywords, count):
    urls = deepsix.download.flickr.urls_tagged(
        keywords,
        api_key='Flickr_API_key.txt')
    deepsix.download.get_images_from_urls(
        urls,
        max_count=count,
        output_directory='images/flickr-new')


def download_target(filename, count):
    urls = deepsix.download.target.iter_sku_url(filename)

    deepsix.download.get_images_from_urls(
        urls,
        max_count=count,
        output_directory='images/target-raw')


def resize(input_directory, output_directory):
    alter_images(
        deepsix.anomalies.resize,
        args=64,
        input_directory=input_directory,
        output_directory=output_directory)


def alter(input_directory, output_directory):
    alter_images(
        procedure=deepsix.anomalies.add_rectangle,
        args=16,
        input_directory=input_directory,
        output_directory=output_directory,
        output_format='BMP'
    )


if __name__ == '__main__':
    # create(10000)
    # create_colours(10000)
    # download_flickr('nikon', 30000)
    # resize('images/flickr-raw', 'images/flickr')
    # download_target('Target_SKUs.txt', 140000)
    resize('images/target-64', 'images/target')

    # alter('images/black', 'images/black+rect')
    # alter('images/solid', 'images/solid+rect')
    # alter('images/flickr', 'images/flickr+rect')
    alter('images/target', 'images/target+rect')

    print('Making black+rect dataset...')
    make_dataset('images/black', 'images/black+rect', 'data/black+rect')

    print('Making solid+rect dataset...')
    make_dataset('images/solid', 'images/solid+rect', 'data/solid+rect')

    print('Making flickr+rect dataset...')
    make_dataset('images/flickr', 'images/flickr+rect', 'data/flickr+rect')

    print('Making target+rect dataset...')
    make_dataset('images/target', 'images/target+rect', 'data/target+rect')
