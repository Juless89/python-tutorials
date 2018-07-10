<center>![banner.png](https://cdn.steemitimages.com/DQmXUKa4wD5mekkSu2DesdjCwviNPrLYmLmVngcZfqcqRsy/banner.png)</center>

This tutorial is the first part of a series where different aspects of programming with Python are explained, using Python and public libraries to make useful tools.

---

#### Repository
https://github.com/ianare/exif-py

#### What will I learn

- Install ExifRead
- What is EXIF data
- Extract EXIF data from images
- Process EXIF data
- Analyse images

#### Requirements

- Python3.6
- ExifRead

#### Difficulty

- basic

---

### Tutorial



#### Setup
Download the files from [Github](https://github.com/Juless89/python-tutorials/tree/master/EXIF). There are 6 files. The code is contained in `exif.py` the other 5 files are images which can be used to test the code on. `exif.py` takes 1 argument which is the filename for the image. In addition, the argument `analysis` is used to perform a model analysis on all the images.

Run scripts as following:
`> python exif.py 1.jpg`

#### Install ExifRead
Installation of the required package is recommended using the PyPI package manager.

```
pip install exifread
```

#### What is EXIF data

Also referred to as `metadata`. When taking a photo the device stores a lot of additional information inside the image file. Information like the `datetime` and `location` or more specific data like the`ISO`, `aperture` and `focal length`.  This information can be used by photographers when comparing images to see which settings worked best, learning from other photographers by looking at which settings they used or data analysis.

<center>
![Screenshot 2018-07-10 16.19.36.png](https://cdn.steemitimages.com/DQmPKr1hAivopVWxt4ArC9pAKai8Z1RLEkJM8HsNuu9CBq6/Screenshot%202018-07-10%2016.19.36.png)
(Right click->get info (for Mac))
</center>

#### Extract EXIF data from images
Processing the image with `exifread.process_image()` returns a dictionary containing all the `EXIF` data.
```
def process_image(filename):
    # Open image file for reading (binary mode)
    f = open(filename, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f)
    return tags
```
<br>
Quite a lot of information can be stored which also adds to the image file size. Photographer can choice to omit` EXIF` data to to save on bandwidth or to keep information about their ways of working private.
```
{
	'Image Make': (0x010F) ASCII = SONY @ 110,
	'Image Model': (0x0110) ASCII = ILCE - 7 M3 @ 116,
	'Image XResolution': (0x011A) Ratio = 240 @ 126,
	'Image YResolution': (0x011B) Ratio = 240 @ 134,
	'Image ResolutionUnit': (0x0128) Short = Pixels / Inch @ 66,
  .
  .
  .
}
```
[Pastebin to the entire EXIF](https://pastebin.com/QwcEJvwE)


#### Process EXIF data
Photographers often share the main settings used for capturing a photo and what gear was used. For this example the data will be extracted from the the image and put into a `html table` for easy sharing. The same works for applying the code on a downloaded image from the web, learning more how the image was taken. The code can easily be adjusted depending on which data is needed.

```
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
```

#### Analyse images
Imagine having a batch of images and you want to know which camera was used the most often. By looping through all the images, creating keys for unique camera models with a value indicating their frequency this can be easily answered.

```
def perform_analysis():
    # Empty dict
    camera_models = {}

    # Loop through images 1-5.jpg
    for image_num in range(1, 6):
        filename = f'{image_num}.jpg'
        # Extract str from the IfdTag
        model = str(process_image(filename)['Image Model'])

        # Fill dict with unique models and increase frequency
        if model in camera_models:
            camera_models[model] += 1
        else:
            camera_models[model] = 1

    print(camera_models)
```

#### Running the code
Five photos come with the code, running `exif.py` on the first three of them shows how useful `EXIF` data is when working with different cameras and different lenses.

---

![1.jpg](https://cdn.steemitimages.com/DQmZcvatWYFzKUCV46pfwiiMUEGk2Y3Bh88fNsQymrM8z2N/1.jpg)

```
python exif.py 1.jpg

```

<table>
<tr><td>Settings</td><td><b>ISO 100 192  mm f/11 3/5 sec </b></td></tr>
<tr><td>Camera</td><td><b>SONY ILCE-7M3</b></td></tr>
<tr><td>Lens</td><td><b>FE 70-200mm F4 G OSS</b></td></tr>
<tr><td>Date</td><td><b>2018:07:04 20:56:11</b></td></tr>
</table>
<br>

![2.jpg](https://cdn.steemitimages.com/DQmPKS8zxS6Pw7dQKUayb9xoeRW4TdUYSz1QmyTtX1RgtLs/2.jpg)

```
python exif.py 2.jpg

```

<table>
<tr><td>Settings</td><td><b>ISO 3200 50  mm f/16/5 1/60 sec </b></td></tr>
<tr><td>Camera</td><td><b>NIKON CORPORATION NIKON D7500</b></td></tr>
<tr><td>Lens</td><td><b>50.0 mm f/1.8</b></td></tr>
<tr><td>Date</td><td><b>2017:12:17 17:24:47</b></td></tr>
</table>
<br>

![3.jpg](https://cdn.steemitimages.com/DQmPfTJ1JNtCb4UBJk43isNvG9EwksMRBLcg56zkeqCxog2/3.jpg)

```
python exif.py 3.jpg

```

<table>
<tr><td>Settings</td><td><b>ISO 100 32  mm f/25 13 sec </b></td></tr>
<tr><td>Camera</td><td><b>NIKON CORPORATION NIKON D3400</b></td></tr>
<tr><td>Lens</td><td><b>18.0-140.0 mm f/3.5-5.6</b></td></tr>
<tr><td>Date</td><td><b>2018:05:11 01:46:48</b></td></tr>
</table>
<br>

Using the argument `analysis` will perform the analysis, looping over all the images and counting which model camera where used with what frequency.

```
python exif.py analysis

{'ILCE-7M3': 3, 'NIKON D7500': 1, 'NIKON D3400': 1}

```

---

The code for this tutorial can be found on [Github](https://github.com/Juless89/python-tutorials/tree/master/EXIF)!

This tutorial was written by @juliank.
