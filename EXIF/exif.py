import exifread
import urllib.request
import random


def downloader(image_url):
    file_name = random.randrange(1,10000)
    full_file_name = str(file_name) + '.jpg'
    urllib.request.urlretrieve(image_url, full_file_name)
    return full_file_name

filename = downloader('https://steemitimages.com/0x0/https://cdn.steemitimages.com/DQmR5fKNdvBtTt35oHjTo2s8pkSJV9kaeyG5YeWTvVvY8V9/76.jpg')


# Open image file for reading (binary mode)
f = open(filename, 'rb')


# Return Exif tags
tags = exifread.process_file(f)
print(tags)


print(tags['Image Make'], tags['Image Model'])
print(tags['Image DateTime'])
print(tags['EXIF ExposureTime'])
print(tags['EXIF FNumber'])
print(tags['EXIF ISOSpeedRatings'])
print(tags['EXIF LensModel'])



#for tag in tags.keys():
    #if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
        #print("Key: %s, value %s" % (tag, tags[tag]))
