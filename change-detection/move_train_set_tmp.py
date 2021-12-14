import os
import sys
import cv2
import json
import shutil


src_dir = r'F:\yang.xie\projects\20211115_data_view\chaosheng\Classify_0\label'
cmp_dir = r'F:\yang.xie\projects\20211115_data_view\chaosheng\Classify_0\train_set_add_roi_name_score\label'
dst_dir = r'F:\yang.xie\projects\20211115_data_view\chaosheng\Classify_0\train_label'

if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)
for one_file in os.listdir(cmp_dir):
    shutil.copy(src_dir + '/' + one_file, dst_dir + '/' + one_file)






