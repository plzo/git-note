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
				cursor = c.execute("SELECT id FROM Detection_0 WHERE selected == 1")
		else:
			try:
				cursor = c.execute("SELECT id FROM RegClassify_0 WHERE selected == 2")
			except:
				cursor = c.execute("SELECT id FROM Detection_0 WHERE selected == 2")
		return [row[0] for row in cursor]

def get_label_suffix(project_dir):
	for one_label in os.listdir(project_dir + '/label'):
		if one_label.endswith('.aqlabel'):
			return '.aqlabel'
		elif one_label.endswith('.json'):
			return '.json'
	print('Label suffix error!')
	return ''

def split_train_test(project_dir,source_dir = ''):
	if source_dir == '':
		source_dir = project_dir + '/source'
	src_label_dir = project_dir + '/label'
	
	dst_dir = source_dir + '/../split_train_test'
	dst_train_dir = dst_dir + '/train'
	dst_test_dir = dst_dir + '/test'

	if not os.path.exists(dst_train_dir):
		os.makedirs(dst_train_dir)
	if not os.path.exists(dst_test_dir):
		os.makedirs(dst_test_dir)

	suffix = get_label_suffix(project_dir)
	train_set = get_list(project_dir,'train')
	test_set = get_list(project_dir,'test')

	for one_source in os.listdir(source_dir):
		index = one_source.split('.')[0]
		one_label = index + suffix
		if int(index) in train_set:
			shutil.copy(src_label_dir + '/' + one_label, dst_train_dir + '/' + one_label)
		elif int(index) in test_set:
			shutil.copy(src_label_dir + '/' + one_label, dst_test_dir + '/' + one_label)
		else:
			print('both train and test can not find index: ',index)


if __name__ == '__main__':
	# project_dir = r'D:\yang.xie\aidi_projects\20201117-iteration4\iter04\RegClassify_0'
	# source_dir = r'D:\yang.xie\aidi_projects\20201203-ROI-bias\generate_label\Detection_0\source'
	# # split_train_test(project_dir,source_dir)

	# source_ok_dir = r'D:\yang.xie\aidi_projects\20201117-iteration4\iter04\OK\source'
	# split_train_test(project_dir,source_ok_dir)
	

	project_dir = r'D:\yang.xie\aidi_projects\20210105-multi-cls\tian_jin_dian_zhuang\Detection_0'
	split_train_test(project_dir)





					



