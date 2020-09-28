import os
import sys
import shutil
import json
import random

def fix_data_info_json(data_info_json_dir,json_dir):
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
	data_info_json_str = open(data_info_json_dir + '/dataset_info.json','r', encoding='UTF-8')
	data_info_json_dict = json.load(data_info_json_str)
	tmp_dict = data_info_json_dict
	json.dump(tmp_dict, open(data_info_json_dir + '/dataset_info_bak.json', 'w',encoding='UTF-8'),ensure_ascii=False)	
	data_info_json_dict['label_names'] = class_list
	json.dump(data_info_json_dict, open(data_info_json_dir + '/dataset_info.json', 'w',encoding='UTF-8'),ensure_ascii=False)
	
if __name__ == '__main__':
	data_info_json_dir = 'D:/yang.xie/aidi_projects/update-label0918/reg_cls_all/RegClassify_0'
	json_dir = "D:/yang.xie/aidi_projects/check_class/xbq-b/RegClassify_0/label"
	fix_data_info_json(data_info_json_dir,json_dir)
		





					



