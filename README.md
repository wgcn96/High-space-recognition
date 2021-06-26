# 操作指引

## 一、矫正图片方向
运行```resave.py```

## 二、
训练命令： python train.py --data data/Web_GlassAndHat.data --cfg cfg/yolov3-tiny.cfg --epochs 200 --weights weights/yolov3-tiny.weights

测试命令：python detect.py --cfg cfg/yolov3-tiny.cfg --weights weights/best.pt --names data/Web_GlassAndHat.names
————————————————
python detect.py --source bus.jpg --save-txt --nosave  --save-conf