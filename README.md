# ML_YOLOV3
ML_YOLOV3(目标检测)
# ML_YOLOV3
## 1.安装环境
numpy

torch >= 1.1.0

opencv-python

tqdm
## 2.总流程
### 迁移学习
python3 train.py --data data/coco_2cls.data --cfg cfg/yolov3-spp-2cls.cfg --weights weights/converted.pt --transfer

(下边这句不对，会报维度的问题)
python3 train.py --data data/coco_2cls.data --cfg cfg/yolov3-spp-2cls.cfg --weights weights/last.pt --transfer
### 测试自己的模型
python3 test.py --data data/coco_1cls.data --weights weights/ultralytics49.pt

python3 test.py --weights weights/last.pt --cfg cfg/yolov3-spp-2cls.cfg --data data/coco_2cls.data
### 检测并且输出结果：
python3 detect.py --weights weights/last.pt --cfg cfg/yolov3-spp-1cls.cfg --data data/coco_1cls.data
## 3.数据集中图片的规格
maxHeight=1040    maxWeight=2008
## 4.lable的归一化处理
https://github.com/ultralytics/yolov3/issues/341

https://github.com/ultralytics/yolov3/issues/524

https://blog.csdn.net/djstavaV/article/details/86743175

def convert(size, box):

    dw = 1./(size[0])
	
    dh = 1./(size[1])
	
    x = (box[0] + box[1])/2.0 - 1
	
    y = (box[2] + box[3])/2.0 - 1
	
    w = box[1] - box[0]
	
    h = box[3] - box[2]
	
    x = x*dw
	
    w = w*dw
	
    y = y*dh
	
    h = h*dh
    return (x,y,w,h)
## 5.使用screen管理后台进程（&创建的后台进程会随着xmanager结束而退出）
(1)screen -S yourname -> 新建一个叫yourname的session

(2)screen -ls         -> 列出当前所有的session

(3)screen -r yourname -> 回到yourname这个session

(4)ctrl+a,d           ->detach当前session

(5)screen -X -S [session # you want to kill] quit

(6)screen -d yourname -> 远程detach某个session

(7)screen -d -r yourname -> 结束当前session并回到yourname这个session
## 6.当网络很差时，安装pytorch可能会超时，解决办法
pip3 --default-timeout=1000 *
## 7.cfg中参数batch的理解
batch=64  每batch个样本更新一次参数。

subdivisions=16 如果内存不够大，将batch分割为subdivisions个子batch，每个子batch的大小为batch/subdivisions。

训练的话把上面注释掉，测试就把训练部分的注释掉
## 8.train.py各个输出结果的含义
https://blog.csdn.net/weixin_42731241/article/details/81474920
## 9.参考项目
代码：https://github.com/ultralytics/yolov3

理论：https://blog.csdn.net/happy990/article/details/89644833
## 10.清理linux的缓存（cache）来增加内存(df -h看磁盘，free -mh看内存)
echo 1 > /proc/sys/vm/drop_caches

echo 2 > /proc/sys/vm/drop_caches

echo 3 > /proc/sys/vm/drop_caches
## 11.常见问题
（1）执行test.py时，使用原默认参数，可以不加任何参数正常运行，这是要在coco_*.data中配置正确的图片路径，
并且images和labels到一一对应，否则会报奇怪的错误

（2）python3 init_image_labels.py --np "/home/dc2-user/ML_YOLOV3/data/emp.txt" --ip "/home/dc2-user/test" --lp "/home/dc2-user/test_ann"




