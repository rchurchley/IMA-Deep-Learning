import deepsix.collection
import deepsix.anomalies
import sys


if __name__ == '__main__':
    if len(sys.argv) < 4:
        size = 28
        input_directory = 'images/raw'
        output_directory = 'images/28'
    else:
        size = int(sys.argv[1])
        input_directory = sys.argv[2]
        output_directory = sys.argv[3]

    deepsix.collection.alter_images(deepsix.anomalies.resize,
                                    size,
                                    input_directory=input_directory,
                                    output_directory=output_directory)
