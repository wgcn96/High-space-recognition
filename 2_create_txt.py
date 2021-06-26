import glob
import json
import os
import random
from PIL import Image
import pandas as pd
import shutil

from my_data.utils import create_file


def convert(size, box):
    """坐标转换为中心点坐标+宽高"""
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[2]) / 2.0 - 1
    y = (box[1] + box[3]) / 2.0 - 1
    w = box[2] - box[0]
    h = box[3] - box[1]

    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def create_dataset(csv_path, txt_path):
    invalid_path = []
    df = pd.read_csv(csv_path, sep=',', header=None, names=['sd_uid', 'sd_add_date', 'sd_task_id', 'sd_batch_id', 'image_id', 'sd_result'], usecols=[4, 5])
    # 每张图片处理
    for i in range(len(df)):
        image_id = df['image_id'][i].split('/')[1].split('.')[0]
        sd_result = df['sd_result'][i]
        print('图片id：', image_id)

        # 获取图片信息（高和宽）
        if os.path.exists('resave/%s.jpg' % image_id):
            img = Image.open('resave/%s.jpg' % image_id)
        else:
            invalid_path.append('resave/%s.jpg' % image_id)
            continue
        size = img.size
        width = size[0]
        height = size[1]

        re = json.loads(sd_result)
        items = re['items']
        data = []
        # 同一张图片的不同框
        for item in items:
            geometry = item['meta']['geometry']
            bb = convert(size, geometry)
            label = item['labels']['标签']

            col = []
            # 标签类型：1:badge   2:offground     3:ground    4:safebelt
            if label == '监护袖章(红only)':
                # data = '1' + '\t' + str(geometry[0]) + '\t' + str(geometry[1]) + '\t' + str(geometry[2]) + '\t' + str(geometry[3])
                col.append(0)
                col.append(bb[0])
                col.append(bb[1])
                col.append(bb[2])
                col.append(bb[3])
            elif label == 'offground':
                col.append(1)
                col.append(bb[0])
                col.append(bb[1])
                col.append(bb[2])
                col.append(bb[3])
            elif label == 'ground':
                col.append(2)
                col.append(bb[0])
                col.append(bb[1])
                col.append(bb[2])
                col.append(bb[3])
            elif label == 'safebelt':
                col.append(3)
                col.append(bb[0])
                col.append(bb[1])
                col.append(bb[2])
                col.append(bb[3])
            data.append(col)
            print(col)

        # 保存为txt
        dt = pd.DataFrame(data)
        dt.to_csv(txt_path + image_id + '.txt', sep='\t', index=False, header=None, encoding="utf-8")
    print('缺失图片数量：', len(invalid_path))
    print(invalid_path)


def split(train_percent, val_percent, file_path):
    total_txt = os.listdir(file_path)
    num = len(total_txt)
    list_index = range(num)
    tv = int(num * val_percent)
    tr = int(tv * train_percent)
    train_all = random.sample(list_index, tv)
    train = random.sample(train_all, tr)

    file_test = open('imagesSets/main' + '/test.txt', 'w', encoding='utf-8')
    file_train = open('imagesSets/main' + '/train.txt', 'w', encoding='utf-8')
    file_val = open('imagesSets/main' + '/val.txt', 'w', encoding='utf-8')

    for i in list_index:
        img_name = total_txt[i][:-4]
        resave_path = 'resave/'+img_name + '.jpg'
        if i in train_all:
            print(i)
            if i in train:
                file_train.write('images/train/' + str(i) + '.jpg'+'\n')
                shutil.copy(file_path+'/' + img_name + '.txt', 'labels/train/' + str(i) + '.txt')
                shutil.copy('resave/' + img_name + '.jpg', 'images/train/' + str(i) + '.jpg')
            else:
                file_val.write('images/val/' + str(i) + '.jpg'+'\n')
                shutil.copy(file_path + '/' + img_name + '.txt', 'labels/val/' + str(i) + '.txt')
                shutil.copy('resave/' + img_name + '.jpg', 'images/val/' + str(i) + '.jpg')
        else:
            file_test.write(resave_path+'\n')

    file_train.close()
    file_val.close()
    file_test.close()


# 根据csv生成txt文件
if __name__ == '__main__':
    csvPath = 'raw/3train_rname.csv'
    txtPath = 'annotations/txt/'

    # 初始化，构造文件夹，删除缓存
    create_file(txtPath)
    create_file('images/train/')
    create_file('images/val/')
    create_file('labels/train/')
    create_file('labels/val/')
    create_file('imagesSets/main/')

    # 构造数据集
    create_dataset(csvPath, txtPath)

    # 所有数据集数量
    val_percent = 1.0
    train_percent = 0.9
    split(train_percent, val_percent, txtPath)
