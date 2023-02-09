import os
import sys
import cv2
import json
import shutil
import numpy as np
import plotly.figure_factory as ff

sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *


mix_dir = r'D:\yang.xie\aidi_projects\20210105-multi-cls\tmp_data\mix_73\source'
only128_dir = r'D:\yang.xie\aidi_projects\20210105-multi-cls\tmp_data\crop_resize_128\source'

both_list = []
only128_list = []
mix_list = []

def count_one(one_path):
    img = Image()
    img.from_file(one_path)
    defect_img = image2numpy(img.visual_at(0))
    return defect_img.shape[0]

mix_dir_list = []
for one_img in os.listdir(mix_dir):
    one_path = mix_dir + '/' + one_img
    size = count_one(one_path)
    if size == 128:
        mix_dir_list.append(one_img)
        
for one_img in mix_dir_list:
    if one_img in os.listdir(only128_dir):
        both_list.append(one_img)
    else:
        mix_list.append(one_img)

for one_img in os.listdir(only128_dir):
    if one_img not in mix_dir_list:
        only128_list.append(one_img)
print('both_list:  ',both_list)
print('only128_list:  ',only128_list)
print('mix_list:  ',mix_list)













