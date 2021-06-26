import os
from PIL import Image, ExifTags
import glob

from my_data.utils import create_file


def resave(src_file, tar_file):
    img_file = os.listdir(src_file)
    for img_name in img_file:
        image = Image.open(src_file + img_name)
        if hasattr(image, '_getexif'):  # only present in JPEGs
            e = image._getexif()  # returns None if no EXIF data
            if e is not None:
                exif = dict(e.items())
                if 0x0112 in exif:
                    orientation = exif[0x0112]
                else:
                    orientation = 0
                print(img_name, orientation)
                if orientation == 3:
                    image = image.rotate(180, expand=True)
                elif orientation == 6:
                    image = image.rotate(270, expand=True)
                elif orientation == 8:
                    image = image.rotate(90, expand=True)
        image.save(tar_file + img_name)


if __name__ == '__main__':
    create_file('resave/')
    # 创建预测集文件夹
    create_file('images/test')

    resave('raw/train/', 'resave/')
    resave('raw/test/', 'images/test/')
