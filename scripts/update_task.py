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

def get_list_2():
	indexes = []
	for one_image in os.listdir(project_dir + '/source'):
		index = one_image.split('.')[0]
		indexes.append(int(index))
	return indexes


def update_task(project_dir):
	task_path = project_dir + '/task.json'
	task_json_str = open(task_path,'r', encoding='UTF-8')
	task_json_dict = json.load(task_json_str)
	tmp_dict = task_json_dict
	json.dump(tmp_dict, open(project_dir + '/task_bak.json', 'w',encoding='UTF-8'),ensure_ascii=False)
	train_set = get_list(project_dir,'train')
	# test_set = get_list(project_dir,'test')
	# all_set = train_set + test_set
	# task_json_dict['indexes']['value'] = get_list_2()
	task_json_dict['indexes']['value'] = train_set
	task_json_dict['model_version']['value'] = 'test'
	task_json_dict['module_type']['value'] = 'Classify'
	task_json_dict['root_path']['value'] = project_dir
	json.dump(task_json_dict, open(project_dir + '/task.json', 'w',encoding='UTF-8'),ensure_ascii=False)


	
if __name__ == '__main__':

	project_dir = r'F:\yang.xie\projects\20220525_pcb\cls_png_v2.3_backup_20230522\Classify_0'
	update_task(project_dir)
		

