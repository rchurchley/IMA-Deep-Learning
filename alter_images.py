import deepsix.collection
import deepsix.anomalies
import sys


if __name__ == '__main__':
    if len(sys.argv) < 3:
        input_directory = 'images/28'
        output_directory = 'images/28-anomalized'
    else:
        input_directory = sys.argv[1]
        output_directory = sys.argv[2]

    deepsix.collection.alter_images(
        procedure=deepsix.anomalies.add_circle,
        args=[],
        input_directory=input_directory,
        output_directory=output_directory,
        output_format='BMP'
    )
