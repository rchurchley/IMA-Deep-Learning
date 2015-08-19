import deepsix
from deepsix import *
from deepsix.download import *
from deepsix.tidy import make_dataset
from deepsix.utils import ensure_directory, alter_images
import IPython
from PIL import Image


def download(keywords, count):
    urls = deepsix.download.flickr.urls_tagged(
        keywords,
        api_key='Flickr_API_key.txt')

    deepsix.download.get_images_from_urls(
        urls,
        max_count=count,
        output_directory='images/flickr-raw')


def create(number):
    ensure_directory('images/black')
    for i in range(1, number + 1):
        Im = Image.new('L', [64, 64], color=0)
        Im.save('images/black/{}.bmp'.format(i), 'BMP')


def create_colours(number):
    ensure_directory('images/solid')
    for i in range(1, number + 1):
        Im = Image.new('L', [64, 64], color=0)
        Im.save('images/solid/{}.bmp'.format(i), 'BMP')


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
    create(5000)
    alter('images/black', 'images/black+rect')
    make_dataset('images/black', 'images/black+rect', 'data/black+rect')

    create_colours(5000)
    alter('images/solid', 'images/solid+rect')
    make_dataset('images/solid', 'images/solid+rect', 'data/solid+rect')

    download('nikon', 1000)
    resize('images/flickr-raw', 'images/flickr')
    alter('images/flickr', 'images/flickr+rect')
    make_dataset('images/flickr', 'images/flickr+rect', 'data/flickr+rect')
