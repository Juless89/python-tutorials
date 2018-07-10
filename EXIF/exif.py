import exifread
import sys


def create_table(tags):
    # extract required data
    brand = tags['Image Make']
    model = tags['Image Model']
    date = tags['Image DateTime']
    shutterspeed = tags['EXIF ExposureTime']
    focallength = tags['EXIF FocalLength']
    aperture = tags['EXIF FNumber']
    iso = tags['EXIF ISOSpeedRatings']
    lens = tags['EXIF LensModel']

    # generate a htlm table
    print('<table>')
    print(f'<tr><td>Settings</td><td><b>ISO {iso} {focallength} ' +
          f' mm f/{aperture} {shutterspeed} sec </b></td></tr>')
    print(f'<tr><td>Camera</td><td><b>{brand} {model}</b></td></tr>')
    print(f'<tr><td>Lens</td><td><b>{lens}</b></td></tr>')
    print(f'<tr><td>Date</td><td><b>{date}</b></td></tr>')
    print('</table>')


def process_image(filename):
    # Open image file for reading (binary mode)
    f = open(filename, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f)
    return tags


if __name__ == '__main__':
    # Filter and process command line arguments
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        tags = process_image(filename)
        create_table(tags)
    else:
        print('Requires 1 image filename as an argument')
