import os
import sys
import shutil
import json
import random
import sqlite3


def get_db_file(project_dir):
	for one_file in os.listdir(project_dir + '/..'):
		if one_file.endswith('.db'):
			return project_dir + '/../' + one_file
	print('Can not find db file!')
	return ''

def get_list(project_dir,eval_set):
	db_file = get_db_file(project_dir)			
	with sqlite3.connect(db_file) as conn:
		c = conn.cursor()
		if eval_set == 'train':
			try:
				cursor = c.execute("SELECT id FROM RegClassify_0 WHERE selected == 1")
			except:
				cursor = c.execute("SELECT id FROM Classify_0 WHERE selected == 1")
		else:
			try:
				cursor = c.execute("SELECT id FROM RegClassify_0 WHERE selected == 2")
			except:
				cursor = c.execute("SELECT id FROM Classify_0 WHERE selected == 2")
		return [row[0] for row in cursor]

def get_label_suffix(project_dir):
	for one_label in os.listdir(project_dir + '/label'):
		if one_label.endswith('.aqlabel'):
			return '.aqlabel'
		elif one_label.endswith('.json'):
			return '.json'
	print('Label suffix error!')
	return ''

def update_task(project_dir):
	task_path = project_dir + '/task.json'
	task_json_str = open(task_path,'r', encoding='UTF-8')
	task_json_dict = json.load(task_json_str)

	dst_1_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\cls_1_base\Classify_0'
	dst_2_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\cls_2_roi\Classify_0'
	dst_3_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\cls_3_roi_type\Classify_0'
	dst_4_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\cls_4_roi_name\Classify_0'

	train_set = get_list(project_dir,'train')
	test_set = get_list(project_dir,'test')
	all_set = train_set + test_set

	input_set = train_set

	task_json_dict['indexes']['value'] = input_set
	task_json_dict['model_version']['value'] = 'V1'
	task_json_dict['module_type']['value'] = 'Classify'
	task_json_dict['root_path']['value'] = project_dir
	json.dump(task_json_dict, open(project_dir + '/task.json', 'w',encoding='UTF-8'),ensure_ascii=False)

	# project base 1
	task_json_dict['indexes']['value'] = train_set
	task_json_dict['model_version']['value'] = 'base_v2_combine14'
	task_json_dict['module_type']['value'] = 'Classify'
	task_json_dict['root_path']['value'] = dst_1_dir
	json.dump(task_json_dict, open(dst_1_dir + '/task.json', 'w',encoding='UTF-8'),ensure_ascii=False)

	# project base roi 2
	task_json_dict['indexes']['value'] = train_set
	task_json_dict['model_version']['value'] = 'base_roi_v2_combine14'
	task_json_dict['module_type']['value'] = 'RoiClassify'
	task_json_dict['root_path']['value'] = dst_2_dir
	json.dump(task_json_dict, open(dst_2_dir + '/task.json', 'w',encoding='UTF-8'),ensure_ascii=False)

	# project type 3
	task_json_dict['indexes']['value'] = input_set
	task_json_dict['model_version']['value'] = 'type_v1'
	task_json_dict['module_type']['value'] = 'RoiClassify'
	task_json_dict['root_path']['value'] = dst_3_dir
	json.dump(task_json_dict, open(dst_3_dir + '/task.json', 'w',encoding='UTF-8'),ensure_ascii=False)

	# project name 4
	task_json_dict['indexes']['value'] = input_set
	task_json_dict['model_version']['value'] = 'name_v1'
	task_json_dict['module_type']['value'] = 'RoiClassify'
	task_json_dict['root_path']['value'] = dst_4_dir
	json.dump(task_json_dict, open(dst_4_dir + '/task.json', 'w',encoding='UTF-8'),ensure_ascii=False)


	
if __name__ == '__main__':
	project_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\channel_display\Classify_0'
	update_task(project_dir)
		

