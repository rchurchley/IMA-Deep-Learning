import wget
import sys

def grabImage(num_images):
    '''
    Grabs num_images images from the human_URLs.txt file
    '''
    f = open('human_URLs.txt', 'r')
    i = 0
    for line in f:
        if i == num_images:
            break
        wget.download(line)
        i += 1

if __name__ == '__main__':
    if len(sys.argv) == 1:
        num_images = 1
    else:
        num_images = int(sys.argv[1])
    grabImage(num_images)
