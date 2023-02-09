import os
import sys
import shutil
import json

sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *

dst_1_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\cls_1_base\Classify_0'
dst_2_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\cls_2_roi\Classify_0'
dst_3_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\cls_3_roi_type\Classify_0'
dst_4_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\cls_4_roi_name\Classify_0'

def clear_dir(dir_path):
    for one_file in os.listdir(dir_path):
        one_file_path = dir_path + '/' + one_file
        os.remove(one_file_path)
    print('delete file * :', dir_path)

def clear_project(project_dir):
    clear_dir(project_dir + '/label')
    clear_dir(project_dir + '/source')

def clear_all_data():
    clear_project(dst_1_dir)
    clear_project(dst_2_dir)
    clear_project(dst_3_dir)
    clear_project(dst_4_dir)

    clear_dir(root_dir + '/label')
    clear_dir(root_dir + '/label_type_name')
    clear_dir(root_dir + '/label_type')
    clear_dir(root_dir + '/label_name')
    clear_dir(root_dir + '/source')
    clear_dir(root_dir + '/source_6')
    clear_dir(root_dir + '/source_9_roi')

if __name__ == '__main__':
 
    clear_all_data()





