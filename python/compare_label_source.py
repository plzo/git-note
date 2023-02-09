import os
import sys
import shutil
import json

sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *

root_dir = r'F:\yang.xie\projects\20211115_data_view\chaosheng\Classify_0\train_set_add_roi'
dst_dir = r'F:\yang.xie\projects\20211115_data_view\chaosheng\Classify_0\train_set_add_roi\label_cmp'

if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)
for one_file in os.listdir(root_dir + '/source'):
    shutil.copy(root_dir + '/label/' + one_file.split('.')[0] + '.aqlabel', dst_dir + '/' + one_file.split('.')[0] + '.aqlabel')






