from PIL import Image
import sys
from deepsix.utils import ensure_directory

if __name__ == '__main__':
    if len(sys.argv) < 2:
        size = 64
        number = 30
    else:
        number = sys.argv[1]

    for i in range(1, number + 1):
        Im = Image.new('L', [size, size], color=0)
        ensure_directory('images/{}-empty'.format(size))
        Im.save('images/{}-empty/{}.bmp'.format(size, i), 'BMP')
