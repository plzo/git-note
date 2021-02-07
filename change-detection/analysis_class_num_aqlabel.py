import sys
import os
import json
sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *


def get_name_score(one_label_path):
	in_label = LabelIO()
	in_label.read_from(one_label_path)
	json_label = json.loads(in_label.to_json())
	return json_label['regions'][0]['name'],json_label['regions'][0]['score']

def display_aqlabel(aqlabel_dir):
	class_list = []
	class_dict = {}
	for one_aqlabel in os.listdir(aqlabel_dir):
		class_name,score = get_name_score(os.path.join(aqlabel_dir,one_aqlabel))
		if class_name not in class_list:
			class_list.append(class_name)
			class_dict[class_name] = 1
		else:
			class_dict[class_name] += 1

	class_list = sorted(class_list)
	for one_name in class_list:
		print(one_name,class_dict[one_name])
	for one_name in class_list:
		print(class_dict[one_name])
	
	# list_for_data_info = []
	# for one_name in class_list:
	# 	print('"' + one_name + '" ,')
		

if __name__ == '__main__':
	# label_dir = "D:/yang.xie/aidi_projects/update-label0918/reg_cls_all/RegClassify_0/label"
	# label_dir = "D:/yang.xie/aidi_projects/project-20201022/classify_no_reg/Classify_0/label"
	
	# label_dir = "D:/yang.xie/aidi_projects/cls-seg20201027/base_project/RegClassify_0/label"
	# label_dir = "D:/yang.xie/aidi_projects/cls-seg20201027/data/processed/label_seg_cls_train"
	label_dir = r"D:\yang.xie\aidi_projects\20210129-pcb-newlabel\channel_display\Classify_0\label_type_name"
	display_aqlabel(label_dir)