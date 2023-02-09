import os
import sys
import cv2
import json
import shutil
import numpy as np
import plotly.figure_factory as ff

sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *

def count_one(one_path):
    img = Image()
    img.from_file(one_path)
    print(img.visual_size())
    defect_img = image2numpy(img.visual_at(0))
    return defect_img.shape[0]

def count_dir(aqimg_dir):
    size_list = []
    size_dict = {}
    count = 0
    size_except_128 = []
    multi_scale_list = []
    scale128_list = []
    for one_img in os.listdir(aqimg_dir):
        one_path = aqimg_dir + '/' + one_img
        size = count_one(one_path)
        if size != 128:
            size_except_128.append(size)
            multi_scale_list.append(int(one_img.split('.')[0]))
        else:
            scale128_list.append(int(one_img.split('.')[0]))
        if size not in size_list:
            size_list.append(size)
            size_dict[size] = 1
        else:
            size_dict[size] += 1
        count += 1
        if size == 511:
            print(one_path)
    print(sorted(size_dict.items(), key = lambda kv:(kv[1], kv[0])))
    print(size_dict)
    print(count)
    print(len(multi_scale_list))
    print(scale128_list)

    return size_except_128

def count_one_channel(one_path):
    img = Image()
    img.from_file(one_path)
    return img.visual_size()

def trans_channel(in_path):
    img = Image()
    img_out = Image()
    img.from_file(in_path)
    if img.visual_size() < 2:
        print("error size: ",img.visual_size()," path: ",in_path)
    batch_img = BatchImage([img.visual_at(0),img.visual_at(1)])
    img_out.from_batch(batch_img)
    img_out.to_file(in_path)

def count_aqimg_channel(aqimg_dir):
    error_list = []
    error_list2 = []
    count = 0
    all_num = len(os.listdir(aqimg_dir))
    for one_img in os.listdir(aqimg_dir):
        one_path = aqimg_dir + '/' + one_img
        channel = count_one_channel(one_path)
        if channel != 2:
            error_list.append(one_path)
        count += 1
        if count % 100 == 0:
            print(all_num - count)


    print("befor processing: ")
    for one_path in error_list:
        print(one_path)
        trans_channel(one_path)
        channel = count_one_channel(one_path)
        if channel != 2:
            error_list2.append(one_path)

    print("after processing: ")
    for one_path in error_list2:
        print(one_path)


if __name__ == '__main__':
    # size_list = count_dir(r'D:\yang.xie\aidi_projects\20210105-multi-cls\cls\Classify_0\source')

    count_aqimg_channel(r'F:\yang.xie\data\20211101_PCB\20220526chaosheng\1\source')

    # hist_data = [np.array(size_list)]
    # group_labels = ['size_rate']
    # fig = ff.create_distplot(hist_data, group_labels, bin_size=.2)
    # fig.show()











