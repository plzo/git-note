import os
import sys
import shutil
import json
import random

def display_json(json_dir):
	class_list = []
	class_dict = {}
	for one_json in os.listdir(json_dir):
		json_str = open(os.path.join(json_dir,one_json),'r', encoding='UTF-8')
		json_dict = json.load(json_str)
		class_name = json_dict[0]['label']
		if class_name not in class_list:
			class_list.append(class_name)
			class_dict[class_name] = 1
		else:
			class_dict[class_name] += 1
	for one_name in class_list:
		print(one_name,class_dict[one_name])
	for one_name in class_list:
		print(class_dict[one_name])
	
		

if __name__ == '__main__':

	# label_dir = "D:/yang.xie/aidi_projects/check_class/xbq-b/RegClassify_0/label"
	# display_json(label_dir)

	label_dir = "D:/yang.xie/aidi_projects/update-label0918/data/数据筛查_json/6通道_fix/label"
	display_json(label_dir)

	






					



