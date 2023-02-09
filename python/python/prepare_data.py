import os
import sys
import shutil
import json

sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *

root_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\channel_display\Classify_0'

dst_1_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\cls_1_base\Classify_0'
dst_2_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\cls_2_roi\Classify_0'
dst_3_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\cls_3_roi_type\Classify_0'
dst_4_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\cls_4_roi_name\Classify_0'

label_dir = root_dir + '/label'
image_dir = root_dir + '/source'
output_label = root_dir + '/label_list.txt'
output_image = root_dir + '/image_list.txt'

def makelist_label():
    fp=open(output_label,'w')    
    for one_file in os.listdir(label_dir):
        if one_file.endswith('.aqlabel'):                       
            fp.write(label_dir + '/' + one_file)
            fp.write('\n')      

def makelist_image():
    fp=open(output_image,'w')    
    for one_file in os.listdir(image_dir):
        if one_file.endswith('.aqimg'):                       
            fp.write(image_dir + '/' + one_file)
            fp.write('\n')   

def get_data(src_dir,dst_dir):
    for one_label in os.listdir(src_dir):
        src_label_path = src_dir + '/' + one_label
        dst_label_path = dst_dir + '/' + one_label
        shutil.copy(src_label_path, dst_label_path)
    print('move file success:', dst_dir)


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
    src_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\pcb_origin\RegClassify_0'

    clear_all_data()

    get_data(src_dir + '/label',root_dir + '/label')
    get_data(src_dir + '/source',root_dir + '/source')
 
    makelist_label()
    makelist_image()
