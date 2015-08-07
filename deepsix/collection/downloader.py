import wget


def get_images_from_urls(image_urls, output_folder="downloads"):
    """Download a list of images from urls with wget."""
    for url in image_urls:
        wget.download(url, out=output_folder)
