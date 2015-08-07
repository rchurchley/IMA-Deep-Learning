import wget
import cv2
import os


def get_images_from_urls(image_urls, output_folder="images/raw"):
    """Download a list of images from urls with wget."""
    for url in image_urls:
        wget.download(url, out=output_folder)


def crop_image(filename, output_filename, crop_height, crop_width):
    """Crop an image to a desired height and width, and save to outfile."""
    img = cv2.imread(filename)
    rows = img.shape[0]
    cols = img.shape[1]
    horiz_border = (rows - crop_height) / 2.
    vert_border = (cols - crop_width) / 2.
    cropped_img = img[horiz_border:rows - horiz_border,
                      vert_border:cols - vert_border]
    cv2.imwrite(output_filename, cropped_img)


def crop_images(
    input_directory='images/raw',
    output_directory='images/cropped',
    crop_height=300,
    crop_width=300
):
    for filename in os.listdir(input_directory):
        root, ext = os.path.splitext(filename)
        if ext == '.jpg' or ext == '.jpeg':
            crop_image(
                input_directory + "/" + filename,
                output_directory + "/" + filename,
                crop_height,
                crop_width
            )
