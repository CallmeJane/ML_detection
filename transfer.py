import os
import cv2
max_height=1040
max_weight=2008

def create_str_to_txt(name, data):
    path_file_name = '/home/dc2-user/trans/%s' % name
    if not os.path.exists(path_file_name):
        with open(path_file_name, "w") as f:
            print(f)

    with open(path_file_name, "a") as f:
        if (data != ""):
            f.write(data)
            f.write('\n')

def read(filename,image_dir):
    with open(filename, encoding='utf-8') as f:
        data = f.readlines()
        for line in data:
            odom = line.split()
            lst = (list(odom))
            print(lst)
            lst_new = []
            if lst[1] == '带电芯充电宝':
                lst_new.append(1)
            elif lst[1] == '不带电芯充电宝':
                lst_new.append(0)
            else:
                input = ""
                name = filename
                create_str_to_txt(name,input)
                continue
            img = cv2.imread(image_dir + filename[0:-3]+'jpg')
            print(image_dir + filename[0:-3]+'jpg')
            sp = img.shape
            height_image=sp[0]
            width_image=sp[1]
            x_center = (float(lst[2]) + float(lst[4])) / 2 - 1
            y_center = (float(lst[3]) + float(lst[5])) / 2 - 1
            width = float(lst[4]) - float(lst[2])
            height = float(lst[5]) - float(lst[3])

            lst_new.append(round(x_center / width_image,5))
            lst_new.append(round(y_center / height_image,5))
            lst_new.append(round(width / width_image,5))
            lst_new.append(round(height / height_image,5))

            input =str(lst_new).replace("[","").replace("]","").replace(","," ")
            print(input)
            name = filename
            create_str_to_txt(name, input)

image_dir="/home/dc2-user/ML_YOLOV3/data/coco/images/"
os.chdir("/home/dc2-user/temp")
for filename in os.listdir():
    print(filename)
    read(filename,image_dir)
