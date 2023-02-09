import os
import sys
import shutil
import json
import random

def add_level(data_info_json_path):
	data_info_json_str = open(data_info_json_path,'r', encoding='UTF-8')
	data_info_json_dict = json.load(data_info_json_str)
	new_list = []

	for one_name in data_info_json_dict['label_names']:
		if one_name != 'OK':
			new_list.append(one_name + '_轻度')
			new_list.append(one_name + '_中度')
			new_list.append(one_name + '_严重')
		else:
			new_list.append(one_name)
	data_info_json_dict['label_names'] = new_list
	json.dump(data_info_json_dict, open(data_info_json_path, 'w',encoding='UTF-8'),ensure_ascii=False)


if __name__ == '__main__':
	json_path = "D:/yang.xie/aidi_projects/20201117-iteration4/classify_no_reg_3level/Classify_0/dataset_info.json"
	add_level(json_path)
		





					



