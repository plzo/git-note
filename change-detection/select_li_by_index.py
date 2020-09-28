import os
import sys
import shutil
import json
import random

def select_il_by_index(image_dir, label_dir, index_dir, out_root_dir):
	if not os.path.exists(out_root_dir + '/test/source'):
		os.makedirs(out_root_dir + '/test/source')
	if not os.path.exists(out_root_dir + '/test/label'):
		os.makedirs(out_root_dir + '/test/label')
	if not os.path.exists(out_root_dir + '/train/source'):
		os.makedirs(out_root_dir + '/train/source')
	if not os.path.exists(out_root_dir + '/train/label'):
		os.makedirs(out_root_dir + '/train/label')

	single_set_list = []
	for one_file in os.listdir(index_dir):
		single_set_list.append(one_file.strip().split('.')[0])

	for one_source in os.listdir(image_dir):
		one_source_path = image_dir + '/' + one_source
		one_label_path = label_dir + '/' + one_source.strip().split('.')[0] + '.aqlabel'

		if one_source.strip().split('.')[0] in single_set_list:
			dst_one_source_path = out_root_dir + '/test/source/' + one_source
			dst_one_label_path = out_root_dir + '/test/label/' + one_source.strip().split('.')[0] + '.aqlabel'
		else:
			dst_one_source_path = out_root_dir + '/train/source/' + one_source
			dst_one_label_path = out_root_dir + '/train/label/' + one_source.strip().split('.')[0] + '.aqlabel'		
		shutil.copy(one_source_path, dst_one_source_path)
		shutil.copy(one_label_path, dst_one_label_path)


def select_il_by_index2(image_dir, label_dir, index_dir, out_root_dir):
	if not os.path.exists(out_root_dir + '/source'):
		os.makedirs(out_root_dir + '/source')
	if not os.path.exists(out_root_dir + '/label'):
		os.makedirs(out_root_dir + '/label')

	single_set_list = []
	for one_file in os.listdir(index_dir):
		single_set_list.append(one_file.strip().split('.')[0])

	for one_source in os.listdir(image_dir):
		one_source_path = image_dir + '/' + one_source.strip().split('.')[0] + '.aqimg'
		one_label_path = label_dir + '/' + one_source.strip().split('.')[0] + '.aqlabel'

		if one_source.strip().split('.')[0] in single_set_list:
			dst_one_source_path = out_root_dir + '/source/' + one_source.strip().split('.')[0] + '.aqimg'
			dst_one_label_path = out_root_dir + '/label/' + one_source.strip().split('.')[0] + '.aqlabel'	
			shutil.copy(one_source_path, dst_one_source_path)
			shutil.copy(one_label_path, dst_one_label_path)


def select_il_by_index3(image_dir, label_dir, index_dir, out_root_dir):
	if not os.path.exists(out_root_dir + '/source'):
		os.makedirs(out_root_dir + '/source')
	if not os.path.exists(out_root_dir + '/label'):
		os.makedirs(out_root_dir + '/label')

	single_set_list = []
	for one_file in os.listdir(index_dir):
		single_set_list.append(one_file.strip().split('.')[0])

	for one_source in os.listdir(image_dir):
		one_source_path = image_dir + '/' + one_source.strip().split('.')[0] + '.xml'
		one_label_path = label_dir + '/' + one_source.strip().split('.')[0] + '.json'

		if one_source.strip().split('.')[0] in single_set_list:
			dst_one_source_path = out_root_dir + '/source/' + one_source.strip().split('.')[0] + '.xml'
			dst_one_label_path = out_root_dir + '/label/' + one_source.strip().split('.')[0] + '.json'	
			shutil.copy(one_source_path, dst_one_source_path)
			shutil.copy(one_label_path, dst_one_label_path)

	
if __name__ == '__main__':

	# use1
	# image_dir = 'D:/yang.xie/aidi_projects/update-label0918/data/source_aqimg'
	# label_dir = 'D:/yang.xie/aidi_projects/update-label0918/data/label_aqlabel'
	# index_dir = 'D:/yang.xie/aidi_projects/update-label0918/data/测试6通道/source'
	# out_root_dir = 'D:/yang.xie/aidi_projects/update-label0918/data/split_2_train_test'
	# select_il_by_index(image_dir, label_dir, index_dir, out_root_dir)

	# use2  aqimg aqlabel
	# image_dir = 'D:/yang.xie/aidi_projects/update-label0918/data/source_aqimg'
	# label_dir = 'D:/yang.xie/aidi_projects/update-label0918/data/label_aqlabel'
	# index_dir = 'D:/yang.xie/aidi_projects/check_class/trueok/source'
	# out_root_dir = 'D:/yang.xie/aidi_projects/update-label0918/data/ok_fix'
	# select_il_by_index2(image_dir, label_dir, index_dir, out_root_dir)

	# use3  xml json
	image_dir = 'D:/yang.xie/aidi_projects/check_class/xbq-b/RegClassify_0/source'
	label_dir = 'D:/yang.xie/aidi_projects/check_class/xbq-b/RegClassify_0/label'
	index_dir = 'D:/yang.xie/aidi_projects/update-label0918/data/数据筛查/6通道_fix/source'
	out_root_dir = 'D:/yang.xie/aidi_projects/update-label0918/data/数据筛查_json/6通道_fix'
	select_il_by_index3(image_dir, label_dir, index_dir, out_root_dir)






					



