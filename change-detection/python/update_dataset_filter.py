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


def get_name_score(one_label_path):
    in_label = LabelIO()
    in_label.read_from(one_label_path)
    json_label = json.loads(in_label.to_json())
    return json_label['regions'][0]['name'],json_label['regions'][0]['score']

def get_class_list(aqlabel_dir):
    class_list = []
    class_dict = {}
    for one_aqlabel in os.listdir(aqlabel_dir):
        class_name,score = get_name_score(os.path.join(aqlabel_dir,one_aqlabel))
        if class_name not in class_list:
            class_list.append(class_name)
            class_dict[class_name] = [one_aqlabel]
        else:
            class_dict[class_name].append(one_aqlabel)

    class_list = sorted(class_list)
    delete_label = []
    choose_list = []

    print('all data: ')
    for one_name in class_list:
        if one_name == 'OK':
            choose_list.append(one_name)
            continue
        if len(one_name.split('-')) == 2 and one_name.split('-')[1] == 'OK':
            choose_list.append(one_name)
            continue
        if len(class_dict[one_name]) < 10:
            delete_label = delete_label + class_dict[one_name]
        else:
            choose_list.append(one_name)

        print(one_name,len(class_dict[one_name]))
    print('choose data: ')
    for one_name in choose_list:
        print(one_name,len(class_dict[one_name]))
   
    return delete_label


def data_filter(src_project_dir,label_dir):
    src_project_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\channel_display\Classify_0'

    delete_label = get_class_list(src_project_dir + '/' + label_dir)

    for one_label in delete_label:
        one_image = one_label.split('.')[0] + '.aqimg'
        os.remove(src_project_dir + '/label/' + one_label)
        os.remove(src_project_dir + '/label_type_name/' + one_label)
        os.remove(src_project_dir + '/label_type/' + one_label)
        os.remove(src_project_dir + '/label_name/' + one_label)
        os.remove(src_project_dir + '/source/' + one_image)
        os.remove(src_project_dir + '/source_6/' + one_image)
        os.remove(src_project_dir + '/source_9_roi/' + one_image)


def move_dir(src_dir,dst_dir):
	for one_label in os.listdir(src_dir):
		src_label_path = src_dir + '/' + one_label
		dst_label_path = dst_dir + '/' + one_label
		shutil.copy(src_label_path, dst_label_path)
	print('move file success:', dst_dir)
	
		
def update_dataset(src_root_dir):
	move_dir(src_root_dir + '/source_6',dst_1_dir + '/source')	
	move_dir(src_root_dir + '/source_9_roi',dst_2_dir + '/source')
	move_dir(src_root_dir + '/source_9_roi',dst_3_dir + '/source')
	move_dir(src_root_dir + '/source_9_roi',dst_4_dir + '/source')

	move_dir(src_root_dir + '/label_type_name',dst_1_dir + '/label')
	move_dir(src_root_dir + '/label_type_name',dst_2_dir + '/label')
	move_dir(src_root_dir + '/label_type',dst_3_dir + '/label')
	move_dir(src_root_dir + '/label_name',dst_4_dir + '/label')

if __name__ == '__main__':
    src_project_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\channel_display\Classify_0'
    label_dir = 'label_type_name'

    data_filter(src_project_dir,label_dir)
    clear_all_data()
    update_dataset(src_project_dir)





