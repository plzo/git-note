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


if __name__ == '__main__':
    aqimg_dir = r'D:\yang.xie\aidi_projects\20210105-multi-cls\cls\Classify_0\source'
    size_list = count_dir(aqimg_dir)
    # hist_data = [np.array(size_list)]
    # group_labels = ['size_rate']
    # fig = ff.create_distplot(hist_data, group_labels, bin_size=.2)
    # fig.show()











