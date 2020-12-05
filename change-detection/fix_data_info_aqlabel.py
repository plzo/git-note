import os
import sys
import shutil
import json
import random

sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *

def get_name_score(one_label_path):
	in_label = LabelIO()
	in_label.read_from(one_label_path)
	json_label = json.loads(in_label.to_json())
	return json_label['regions'][0]['name'],json_label['regions'][0]['score']

def get_list(aqlabel_dir):
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
	return class_list

def fix_data_info_aqlabel(project_dir):
	class_list = get_list(project_dir + '/label')
	data_info_json_str = open(project_dir + '/dataset_info.json','r', encoding='UTF-8')
	data_info_json_dict = json.load(data_info_json_str)
	tmp_dict = data_info_json_dict
	json.dump(tmp_dict, open(project_dir + '/dataset_info_bak.json', 'w',encoding='UTF-8'),ensure_ascii=False)	
	data_info_json_dict['label_names'] = class_list
	json.dump(data_info_json_dict, open(project_dir + '/dataset_info.json', 'w',encoding='UTF-8'),ensure_ascii=False)
	
if __name__ == '__main__':
	project_dir = r'D:\yang.xie\aidi_projects\20201203-ROI-bias\cls\Classify_0'
	fix_data_info_aqlabel(project_dir)


		





					



