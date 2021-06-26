import os

from PIL import Image


def is_valid_image(img_path):
    """
    判断文件是否为有效（完整）的图片
    :param img_path:图片路径
    :return:True：有效 False：无效
    """
    bValid = True
    try:
        Image.open(img_path).verify()
    except:
        bValid = False
    return bValid


def transimg(img_path):
    """
    转换图片格式
    :param img_path:图片路径
    :return: True：成功 False：失败
    """
    if is_valid_image(img_path):
        try:
            str = img_path.rsplit(".", 1)
            output_img_path = str[0] + ".jpg"
            print(output_img_path)
            im = Image.open(img_path)
            im.save(output_img_path)
            return True
        except:
            return False
    else:
        return False

"""
把png转jpg
"""
if __name__ == '__main__':
    total_img = os.listdir('raw')
    for img in total_img:
        # 判断是否是png
        if img.split('.')[1] == 'png' or img.split('.')[1] == 'PNG':
            result = transimg('raw/' + img)
            if result:
                os.remove('raw/' + img)
                print('succeed')
            else:
                print('fail')
