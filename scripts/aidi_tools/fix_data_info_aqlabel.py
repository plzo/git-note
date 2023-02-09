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
	res = []
	for one_name in class_list:
		if one_name != '':
			res.append(one_name)
		else:
			print('empty label mum: ',class_dict[one_name])
	return res

def fix_data_info_aqlabel(project_dir):
	dst_1_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\cls_1_base\Classify_0'
	dst_2_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\cls_2_roi\Classify_0'
	dst_3_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\cls_3_roi_type\Classify_0'
	dst_4_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\cls_4_roi_name\Classify_0'

	class_list = get_list(project_dir + '/label_type_name')
	data_info_json_str = open(project_dir + '/dataset_info.json','r', encoding='UTF-8')
	data_info_json_dict = json.load(data_info_json_str)
	data_info_json_dict['label_names'] = class_list
	json.dump(data_info_json_dict, open(project_dir + '/dataset_info.json', 'w',encoding='UTF-8'),ensure_ascii=False)

	data_info_json_dict['xml_base_num'] = 2
	json.dump(data_info_json_dict, open(dst_1_dir + '/dataset_info.json', 'w',encoding='UTF-8'),ensure_ascii=False)

	data_info_json_dict['xml_base_num'] = 3
	json.dump(data_info_json_dict, open(dst_2_dir + '/dataset_info.json', 'w',encoding='UTF-8'),ensure_ascii=False)

	class_list = get_list(project_dir + '/label_type')
	data_info_json_dict['label_names'] = class_list
	json.dump(data_info_json_dict, open(dst_3_dir + '/dataset_info.json', 'w',encoding='UTF-8'),ensure_ascii=False)

	class_list = get_list(project_dir + '/label_name')
	data_info_json_dict['label_names'] = class_list
	json.dump(data_info_json_dict, open(dst_4_dir + '/dataset_info.json', 'w',encoding='UTF-8'),ensure_ascii=False)
	
if __name__ == '__main__':
	project_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\channel_display\Classify_0'
	fix_data_info_aqlabel(project_dir)


		





					



