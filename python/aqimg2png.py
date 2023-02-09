import os
import sys
import cv2
import json
import shutil
import numpy as np
import plotly.figure_factory as ff

sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *

def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def trans_one(input_path, aqimg_name, out_path):
    aqimg_path = os.path.join(input_path,aqimg_name)
    img = Image()
    img.from_file(aqimg_path)
    img_size = img.visual_size()
    for i in range(img_size):
        np_img = image2numpy(img.visual_at(i))
        makedirs(out_path + '/' + str(i))
        cv2.imwrite(out_path + '/' + str(i) + '/' + aqimg_name.split('.')[0] + '_' + str(i) + '.png', np_img)

def trans_all(input_root_path,out_path):
    for one_file in os.listdir(input_root_path):
        trans_one(input_root_path, one_file, out_path)

if __name__ == '__main__':
    input_root_path = r'D:\yang.xie\workspace\change-detection\data\validate\source'
    out_path = r'D:\yang.xie\workspace\change-detection\data\validate\images'
    trans_all(input_root_path,out_path)

