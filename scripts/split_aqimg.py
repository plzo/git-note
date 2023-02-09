import os
import sys
import cv2
import json
import shutil

sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *

def split_one(one_path,out_path1,out_path2):
    img = Image()
    img.from_file(one_path)
    defect_img = image2numpy(img.visual_at(0))
    origin_img = image2numpy(img.visual_at(1))
    cv2.imwrite(out_path1,defect_img)
    cv2.imwrite(out_path2,origin_img)

def get_train_list(json_file):
	json_str = open(os.path.join(json_file),'r', encoding='UTF-8')
	json_dict = json.load(json_str)
	train_list = json_dict['indexes']['value']
	return train_list

def generate_new_task(project_dir,train_list):
    new_list = []
    for one_index in train_list:
        new_list.append(one_index)
        new_list.append(one_index + 20000)
    json_str = open(project_dir + '/task.json','r', encoding='UTF-8')
    json_dict = json.load(json_str)
    json_dict['indexes']['value'] = new_list
    json.dump(json_dict, open(project_dir + '/new_task.json', 'w',encoding='UTF-8'),ensure_ascii=False)

def get_name(one_label_path):
	in_label = LabelIO()
	in_label.read_from(one_label_path)
	tmp = in_label.to_json()
	json_label = json.loads(tmp)
	return json_label['regions'][0]['name']

def get_ok_path(label_dir):
    for one_label in os.listdir(label_dir):
        one_label_path = label_dir + '/' + one_label
        if get_name(one_label_path) == 'OK':
            return one_label_path

def split_aqimg(project_dir):
    if not os.path.exists(project_dir + '/split_source'):
        os.makedirs(project_dir + '/split_source')
    if not os.path.exists(project_dir + '/split_label/train_label'):
        os.makedirs(project_dir + '/split_label/train_label')
    if not os.path.exists(project_dir + '/split_label/test_label'):
        os.makedirs(project_dir + '/split_label/test_label')
    
    train_list = get_train_list(project_dir + '/task.json')
    generate_new_task(project_dir,train_list)
    ok_path = get_ok_path(project_dir + '/label')

    for one_img in os.listdir(project_dir + '/source'):
        str_index = one_img.strip().split('.')[0]
        img_path = project_dir + '/source/' + one_img
        out_path1 = project_dir + '/split_source/' + str_index + '.png'
        out_path2 = project_dir + '/split_source/' + str(int(str_index) + 20000) + '.png'
        split_one(img_path,out_path1,out_path2)

        if int(str_index) in train_list:
            shutil.copy(project_dir + '/label/' + str_index + '.aqlabel', project_dir + '/split_label/train_label/' + str_index + '.aqlabel')
            shutil.copy(ok_path, project_dir + '/split_label/train_label/' + str(int(str_index) + 20000) + '.aqlabel')
        else:
            shutil.copy(project_dir + '/label/' + str_index + '.aqlabel', project_dir + '/split_label/test_label/' + str_index + '.aqlabel')
            shutil.copy(ok_path, project_dir + '/split_label/test_label/' + str(int(str_index) + 20000) + '.aqlabel')


if __name__ == '__main__':

    project_dir = r"D:\yang.xie\aidi_projects\20201117-iteration4\iter04\RegClassify_0"

    # img_path = "D:/yang.xie/data/aqimg3/1.aqimg"
    # out_path1 = "D:/yang.xie/data/aqimg3/01.png"
    # out_path2 = "D:/yang.xie/data/aqimg3/02.png"
    split_aqimg(project_dir)









