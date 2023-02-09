import os
import sys
import cv2
import json
import shutil
import numpy as np
import plotly.figure_factory as ff

sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *


def move_test(src_dir,dst_dir,src_dir2,dst_dir2,task_json):
    task_json_str = open(task_json,'r', encoding='UTF-8')
    task_json_dict = json.load(task_json_str)
    train_set = task_json_dict['indexes']['value']

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for one_index in train_set:
        try:
            shutil.copy(src_dir + '/' + str(one_index) + '.aqlabel', dst_dir + '/' + str(one_index) + '.aqlabel')
            shutil.copy(src_dir2 + '/' + str(one_index) + '.aqimg', dst_dir2 + '/' + str(one_index) + '.aqimg')
        except:
            print(src_dir + '/' + str(one_index) + '.aqlabel')


def move_test2(project_dir):
    task_path = project_dir + '/task.json'
    task_json_str = open(task_path,'r', encoding='UTF-8')
    task_json_dict = json.load(task_json_str)
    train_set = task_json_dict['indexes']['value']
    dst_dir = project_dir + '/train_label_set'

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for one_index in train_set:
        try:
            shutil.copy(project_dir + '/label/' + str(one_index) + '.aqlabel', dst_dir + '/' + str(one_index) + '.aqlabel')
        except:
            print(project_dir + '/label/' + str(one_index) + '.aqlabel')


if __name__ == '__main__':
    # project_dir = r'D:\yang.xie\aidi_projects\20210105-multi-cls\cls_aqimg\Classify_0'
    # move_test(project_dir)

    src_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\pcb_origin\RegClassify_0\label'
    dst_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\pcb_origin\RegClassify_0\test_set\label'
    src_dir2 = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\pcb_origin\RegClassify_0\source'
    dst_dir2 = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\pcb_origin\RegClassify_0\test_set\source'
    task_json = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\20210419_big_set\cls\tasks\cls\test_task.json'
    move_test(src_dir,dst_dir,src_dir2,dst_dir2,task_json)














