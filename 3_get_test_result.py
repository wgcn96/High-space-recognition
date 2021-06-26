import os
import json
import pandas as pd
from PIL import Image


# 把[x,y,w,h]坐标系转换为（左上和右下）.size为图片尺寸，box为中心点坐标与宽高
def reconvert(size, box):
    center_x = round(float(box[0]) * size[0])
    center_y = round(float(box[1]) * size[1])
    bbox_width = round(float(box[2]) * size[0])
    bbox_height = round(float(box[3]) * size[1])

    xmin = int(center_x - bbox_width / 2)
    ymin = int(center_y - bbox_height / 2)
    xmax = int(center_x + bbox_width / 2)
    ymax = int(center_y + bbox_height / 2)
    return xmin, ymin, xmax, ymax


def mat_inter(box1, box2):
    # 判断两个矩形是否相交
    # box=(xA,yA,xB,yB)
    x01, y01, x02, y02 = box1
    x11, y11, x12, y12 = box2

    lx = abs((x01 + x02) / 2 - (x11 + x12) / 2)
    ly = abs((y01 + y02) / 2 - (y11 + y12) / 2)
    sax = abs(x01 - x02)
    sbx = abs(x11 - x12)
    say = abs(y01 - y02)
    sby = abs(y11 - y12)
    if lx <= (sax + sbx) / 2 and ly <= (say + sby) / 2:
        return True
    else:
        return False


def solve_coincide(box1, box2):
    # box=(xA,yA,xB,yB)
    # 计算两个矩形框的重合度
    if mat_inter(box1, box2):
        x01, y01, x02, y02 = box1
        x11, y11, x12, y12 = box2
        col = min(x02, x12) - max(x01, x11)
        row = min(y02, y12) - max(y01, y11)
        intersection = col * row
        area1 = (x02 - x01) * (y02 - y01)
        area2 = (x12 - x11) * (y12 - y11)
        coincide = intersection / (area1 + area2 - intersection)
        return coincide
    else:
        return False


if __name__ == '__main__':
    csv_path = 'raw/3_testa_user.csv'
    img_path = 'images/test/'
    label_path = 'labels/test/'
    df = pd.read_csv(csv_path, sep=',', header=None, names=['id', 'image_url'])

    datas = []
    # 每张图片处理
    for i in range(len(df)):
        image_id = df['id'][i]
        image_name = df['image_url'][i].split('/')[1].split('.')[0]
        print(image_id, image_name)
        # 获取图片信息（高和宽）
        if os.path.exists(img_path + '%s.jpg' % image_name):
            img = Image.open(img_path + '%s.jpg' % image_name)
        else:
            print('图片不存在。')
            continue
        size = img.size
        width = size[0]
        height = size[1]

        # 逐行读取预测的labels，并进行坐标转换
        items = []
        if not os.path.exists(label_path + '%s.txt' % image_name):
            continue
        with open(label_path + '%s.txt' % image_name, "r") as f:
            for line in f.readlines():
                item = []
                line = line.strip('\n').split(' ')

                # 获取类型标签
                label = float(line[0])
                score = float(line[5])

                # 坐标系转换
                box = [float(line[1]), float(line[2]), float(line[3]), float(line[4])]
                bbox = list(reconvert(size, box))

                item.append(label)
                item.append(bbox[0])
                item.append(bbox[1])
                item.append(bbox[2])
                item.append(bbox[3])
                item.append(score)
                items.append(item)

        # 对每张照片进行分析，标签类型：0:badge   1:offground     2:ground    3:safebelt
        for item in items:
            label = item[0]
            box1 = [item[1], item[2], item[3], item[4]]
            print('box1',box1)
            score = item[5]
            # 判断类型
            if label == 1:  # 离地状态的人
                # 创建一个json-离地状态的人
                category_id = 3
                data = {"image_id": int(image_id),
                        "category_id": int(category_id),
                        "bbox": box1,
                        "score": float(score)}
                datas.append(data)

                # 判断是否带安全带、臂章
                for i in items:
                    labl = i[0]
                    if labl == 0:
                        box2 = [i[1], i[2], i[3], i[4]]
                        print('box2', box2)
                        # 判断是否重合臂章
                        if mat_inter(box1, box2):
                            # guarder（监护人员）
                            # 创建一个json-监护人员
                            category_id = 1
                            data = {"image_id": int(image_id),
                                    "category_id": int(category_id),
                                    "bbox": box1,
                                    "score": float(score)}
                            datas.append(data)
                    elif labl == 3:
                        box2 = [i[1], i[2], i[3], i[4]]
                        print('box2', box2)
                        # 判断是否重合安全带
                        if mat_inter(box1, box2):
                            # （佩戴安全带人员）
                            # 创建一个json-佩戴安全带人员
                            category_id = 2
                            data = {"image_id": int(image_id),
                                    "category_id": int(category_id),
                                    "bbox": box1,
                                    "score": float(score)}
                            datas.append(data)
            elif label == 2:  # 着地状态的人
                # 判断是否带安全带、臂章
                for i in items:
                    labl = i[0]
                    if labl == 0:
                        box2 = [i[1], i[2], i[3], i[4]]
                        # 判断是否重合臂章
                        if mat_inter(box1, box2):
                            # guarder（监护人员）
                            # 创建一个json-监护人员
                            category_id = 1
                            data = {"image_id": int(image_id),
                                    "category_id": int(category_id),
                                    "bbox": box1,
                                    "score": float(score)}
                            datas.append(data)
                    elif labl == 3:
                        box2 = [i[1], i[2], i[3], i[4]]
                        # 判断是否重合安全带
                        if mat_inter(box1, box2):
                            # 创建一个json-佩戴安全带人员
                            category_id = 2
                            data = {"image_id": int(image_id),
                                    "category_id": int(category_id),
                                    "bbox": box1,
                                    "score": float(score)}
                            datas.append(data)
    # 将data转为json数组
    with open('result.json', 'w') as FD:
        print(json.dumps(datas))
        FD.write(json.dumps(datas))

