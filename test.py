import os

import pandas as pd
from PIL import Image, ImageDraw


# 把[x,y,w,h]坐标系转换为（左上和右下）.size为图片尺寸，box为中心点坐标与宽高
def recovert(size, box):
    center_x = round(float(box[0]) * size[0])
    center_y = round(float(box[1]) * size[1])
    bbox_width = round(float(box[2]) * size[0])
    bbox_height = round(float(box[3]) * size[1])

    xmin = int(center_x - bbox_width / 2)
    ymin = int(center_y - bbox_height / 2)
    xmax = int(center_x + bbox_width / 2)
    ymax = int(center_y + bbox_height / 2)
    return xmin, ymin, xmax, ymax


if __name__ == '__main__':
    img_path = 'bus.jpg'
    label_path = 'bus.txt'
    # 获取图片信息（高和宽）
    if os.path.exists(img_path):
        img = Image.open(img_path)
    else:
        print('图片不存在。')
    size = img.size
    width = size[0]
    height = size[1]

    bboxs = []
    # 逐行读取预测的labels，并进行坐标转换
    items = []
    with open(label_path, "r") as f:
        for line in f.readlines():
            item = []
            line = line.strip('\n').split(' ')
            label = float(line[0])
            # print(line)
            # print(label)
            box = [float(line[1]), float(line[2]), float(line[3]), float(line[4])]
            # print(box)

            bbox = list(recovert(size,box))
            item.append(label)
            item.append(bbox[0])
            item.append(bbox[1])
            item.append(bbox[2])
            item.append(bbox[3])
            # item.append(score)
            items.append(item)
    print(items)
    #         print(bbox)
    #         bboxs.append(bbox)
    # draw = ImageDraw.Draw(img)
    # for geometry in bboxs:
    #     # bboxs.append(geometry)
    #     draw.rectangle(geometry, width=8, fill=None)
    # img.show()
