import json
import os
from PIL import Image, ImageDraw
import pandas as pd
"""
把标注框画在图片上
"""


def draw(csv_path, img_path, res_path):
    invalid_path = []
    df = pd.read_csv(csv_path, sep=',', header=None, names=['sd_uid', 'sd_add_date', 'sd_task_id', 'sd_batch_id', 'image_id', 'sd_result'], usecols=[4, 5])

    # 每张图片处理
    for i in range(len(df)):
        bboxs = []
        image_id = df['image_id'][i].split('/')[1].split('.')[0]
        sd_result = df['sd_result'][i]
        print('图片id：', image_id)

        # 获取图片信息（高和宽）
        if os.path.exists(img_path+'%s.jpg' % image_id):
            img = Image.open(img_path+'%s.jpg' % image_id)
        else:
            invalid_path.append(img_path+'%s.jpg' % image_id)
            continue
        size = img.size
        width = size[0]
        height = size[1]

        re = json.loads(sd_result)
        items = re['items']
        # 同一张图片的不同框,（左上和右下）
        draw = ImageDraw.Draw(img)
        for item in items:
            geometry = item['meta']['geometry']
            # bboxs.append(geometry)
            draw.rectangle(geometry, width=8, fill=None)
        # img.show()
        img.save(res_path + '%s.jpg' % image_id)


# 根据csv生成txt文件
if __name__ == '__main__':
    csv_path = 'raw/3train_rname.csv'
    img_path = 'resave/'
    res_path = 'img_draw_labels/'
    draw(csv_path, img_path, res_path)

