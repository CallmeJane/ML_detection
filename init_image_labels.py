#coding=utf-8
import sys
import argparse
import linecache
import platform
import os
import cv2
import shutil
coco_2cls_data_path="data/coco_2cls.data"

def create_str_to_txt(name, data):

    if(data==""):
        return
    if not os.path.exists(name):
        f=open(name,"w")
        f.close()
    with open(name, "a") as f:
        if (data != ""):
            f.write(data)
            f.write('\n')

#old lables,names,image_path,new_label_path
def read(label_path,filename,image_path,new_label_path,isWindows):
    with open(label_path+filename+'.txt', encoding='utf-8') as f:
        data = f.readlines()
        for line in data:
            odom = line.split()
            lst = (list(odom))
            #print(lst)
            lst_new = []
            if lst[1] == '带电芯充电宝':
                lst_new.append(1)
            elif lst[1] == '不带电芯充电宝':
                lst_new.append(0)
            else:
                input = ""
                name = label_path
                create_str_to_txt(label_path,input)
                continue
            path=""
            if(isWindows==True):
                path=image_path + '\\' + filename+'.jpg'
            else:
                path=image_path + '/' + filename+'.jpg'
            img = cv2.imread(path)
            sp = img.shape
            height_image=sp[0]
            width_image=sp[1]
            x_center = (float(lst[2]) + float(lst[4])) / 2 - 1
            y_center = (float(lst[3]) + float(lst[5])) / 2 - 1
            width = float(lst[4]) - float(lst[2])
            height = float(lst[5]) - float(lst[3])

            if(x_center>width_image or width>width_image or y_center>height_image or height>height_image):
                input = ""
                name = label_path
                create_str_to_txt(label_path, input)
                continue

            lst_new.append(round(x_center / width_image,5))
            lst_new.append(round(y_center / height_image,5))
            lst_new.append(round(width / width_image,5))
            lst_new.append(round(height / height_image,5))

            input =str(lst_new).replace("[","").replace("]","").replace(","," ")
            #print(input)
            name = new_label_path + filename+'.txt'
            create_str_to_txt(name, input)

def update_2cls(name_path,image_path):
    #读取coco_2cls_data_path的第三行，获取test配置文件的目录
    line_3=linecache.getline(coco_2cls_data_path,3)
    n_pos=line_3.find('=')
    test_config_path=line_3[n_pos+1:-1]
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    test_config_file=open(test_config_path,'a')
    name_file = open(name_path, 'r')

    #判断是windows还是linux系统
    system=platform.system()
    if(system == 'Windows'):
        if(image_path[-1]!='\\'):
            image_path=image_path+'\\'
    else:
        if(image_path[-1]!='/'):
            image_path=image_path+'/'
    for name in name_file:
        ss=image_path+name[:-1]+'.jpg'+'\n'
        test_config_file.write(ss)

    name_file.close()
    test_config_file.close()

def mv_images(name_path,image_path):
    #1.打开name_path
    #2.将所有的图片copy到指定目录
    pass

#将lables标准化，并且在对应目录下创建文件
def trans_labels(name_path,lable_path,image_path):
    #在imgages对应的目录下创建labels目录
    new_labels_path=""
    system=platform.system()
    isWindows=False
    print("system:"+system)
    if(system == 'Windows'):
        isWindows=True
        temp=""
        if(image_path[-1]=='\\'):
            image_path = image_path[0:len(image_path) - 1]
        npos = image_path.rfind('\\')
        if (npos == -1):
            return
        else:
            new_labels_path = image_path[0:npos] + "\\labels\\"
        if(lable_path[-1]!='\\'):
            lable_path=lable_path+'\\'
    else:
        if (image_path[-1] == '/'):
            image_path = image_path[0:len(image_path) - 1]
        npos = image_path.rfind('/')
        print(str(npos))
        if (npos == -1):
            return
        else:
            new_labels_path = image_path[0:npos] + "/labels/"
        if (lable_path[-1] != '/'):
            lable_path = lable_path + '/'
    #创建labels目录
    print("new"+new_labels_path)
    if os.path.exists(new_labels_path):
        pass
    else:
        os.mkdir(new_labels_path)

    #在lables下创建新的文件
    name_file = open(name_path, 'r')
    for name in name_file:
        read(lable_path,name[0:-1], image_path,new_labels_path,isWindows)

def get_all_names(image_path,names):
    f1 = open(names, 'a')
    for filename in os.listdir(image_path):
        f1.write(filename.rstrip('.jpg'))
        f1.write("\n")
        print(filename)
    f1.close()

#接收三个参数：图片名字文件路径(name_path)，图片路径(image_path)，标签路径(labels_path)
#根据当前路径将数据当拷贝到对应的目录下（相对目录）
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='init_image_labels.py')
    parser.add_argument('--np', type=str, default='data/coco/battery_sub_test.txt', help='name_path')
    parser.add_argument('--ip', type=str, default='data/coco/images/', help='image_path')
    parser.add_argument('--lp', type=str, default='data/coco/labels/', help='labels_path')

    opt = parser.parse_args()
    get_all_names(opt.ip,opt.np)
    system = platform.system()
    new_image_path=""
    if (system == 'Windows'):
        curr_path=os.getcwd()
        coco_path=curr_path+"\data\coco"
        if os.path.exists(coco_path)==False:
            os.mkdir(coco_path)
        new_image_path=coco_path+"\images"
        if(os.path.exists(new_image_path)==True):
            shutil.rmtree(new_image_path)
    else:
        curr_path=os.getcwd()
        coco_path=curr_path+"/data/coco"
        if os.path.exists(coco_path)==False:
            os.mkdir(coco_path)
        new_image_path=coco_path+"/images"
        if(os.path.exists(new_image_path)==True):
            shutil.rmtree(new_image_path)

    shutil.copytree(opt.ip,new_image_path)

    print(new_image_path)
    update_2cls(opt.np,new_image_path)
    trans_labels(opt.np, opt.lp, new_image_path)
    print("end!!!")
