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

def get_train_list(json_file):
	json_str = open(os.path.join(json_file),'r', encoding='UTF-8')
	json_dict = json.load(json_str)
	train_list = json_dict['indexes']['value']
	return train_list

def get_level(score):
	if score < 0.45:
		return 1
	elif score < 0.75:
		return 2
	else:
		return 3

def compare_label(label_path,prob_path):
	label_name,label_score = get_name_score(label_path)
	prob_name,prob_score = get_name_score(prob_path)
	if label_name == 'OK' and prob_name == 'OK':
		return 'ok_true'
	elif label_name == 'OK' and prob_name != 'OK':
		return 'ok_over'
	elif label_name != 'OK' and prob_name == 'OK':
		return 'ok_miss'
	else:
		if get_level(label_score) > get_level(prob_score):
			if label_name == prob_name:
				return 'ng_miss_same'
			else:
				return 'ng_miss_diff'
		elif get_level(prob_score) > get_level(label_score):
			if label_name == prob_name:
				return 'ng_over_same'
			else:
				return 'ng_over_diff'
		else:
			if label_name == prob_name:
				return 'same_true'
			else:
				return 'diff_true'

def get_set(root_dir, train_list):
	train_set = []
	test_set = []
	for one_label in os.listdir(root_dir + '/label'):
		index = int(one_label.strip().split('.')[0])
		if index in train_list:
			train_set.append(one_label)
			train_list.remove(index)
		else:
			test_set.append(one_label)
	return train_set,test_set

def eval_one_set(root_dir,train_list):
	test_result_dir = root_dir + '/test_result'
	label_dir = root_dir + '/label'
	compare_res = {'ok_true': 0., 'same_true': 0., 'diff_true': 0., 'ok_miss': 0., 'ng_miss_same': 0., 'ng_miss_diff': 0., 'ok_over': 0., 'ng_over_same': 0., 'ng_over_diff': 0.}
	for one_label in train_list:
		label_path = label_dir + '/' + one_label
		prob_path = test_result_dir + '/' + one_label
		compare_res[compare_label(label_path,prob_path)] += 1
	return compare_res

def add_dict(dict_list):
	if len(dict_list) < 1:
		return {}
	elif len(dict_list) < 2:
		return dict_list[0]
	else:
		for i in range(len(dict_list) - 1):
			for (name, num) in dict_list[i+1].items():
				dict_list[0][name] += num
		return dict_list[0]

def eval_display(compare_res):
	total_num = 0.
	for (name,num) in compare_res.items():
		total_num += num
	acc = (compare_res['ok_true'] + compare_res['same_true'] + compare_res['diff_true']) / total_num
	miss = (compare_res['ok_miss'] + compare_res['ng_miss_same'] + compare_res['ng_miss_diff']) / total_num
	over = (compare_res['ok_over'] + compare_res['ng_over_same'] + compare_res['ng_over_diff']) / total_num
	mix = compare_res['diff_true'] / (compare_res['diff_true'] + compare_res['same_true'])
	aidi_acc = (compare_res['ok_true'] + compare_res['same_true'] + compare_res['ng_miss_same'] + compare_res['ng_over_same']) / total_num
	defect_acc = (compare_res['diff_true'] + compare_res['same_true']) / (total_num - compare_res['ok_true'] - compare_res['ok_over'])
	print('指标列表：\n',compare_res)
	print('漏检率:\n',miss * 100)
	print('过检率:\n',over * 100)
	print('混淆率:\n',mix * 100)
	print('acc:\n',acc * 100)
	print('aidi_acc:\n',aidi_acc * 100)
	print('defect_acc:\n',defect_acc * 100)
	print('total_num,true_num:\n',total_num, total_num * acc)

def eval_level_mixrate(root_dir_list,json_file_list):
	if len(root_dir_list) != len(json_file_list):
		return
	train_dict_list = []
	test_dict_list = []
	for i in range(len(root_dir_list)):
		train_list = get_train_list(json_file_list[i])
		train_set,test_set = get_set(root_dir_list[i], train_list)		
		train_dict = eval_one_set(root_dir_list[i],train_set)	
		test_dict = eval_one_set(root_dir_list[i],test_set)

		train_dict_list.append(train_dict)
		test_dict_list.append(test_dict)

	sum_train_dict = add_dict(train_dict_list)
	sum_test_dict = add_dict(test_dict_list)
	print('train results:')	
	eval_display(sum_train_dict)
	print('test results:')
	eval_display(sum_test_dict)

	
if __name__ == '__main__':
	root_dir_all = 'D:/yang.xie/aidi_projects/update-label0918/reg_cls_all/RegClassify_0'
	json_file_all = root_dir_all + '/task.json'
	root_dir_double = 'D:/yang.xie/aidi_projects/update-label0918/reg_cls_double/RegClassify_0'
	json_file_double = root_dir_double + '/task.json'
	root_dir_single = 'D:/yang.xie/aidi_projects/update-label0918/reg_cls_single/RegClassify_0'
	json_file_single = root_dir_single + '/task.json'

	print('********************reg_cls_all*********************')
	eval_level_mixrate([root_dir_all],[json_file_all])
	print('********************reg_cls_double*********************')
	eval_level_mixrate([root_dir_double],[json_file_double])
	print('********************reg_cls_single*********************')
	eval_level_mixrate([root_dir_single],[json_file_single])
	print('********************reg_cls_double single*********************')
	eval_level_mixrate([root_dir_double,root_dir_single],[json_file_double,json_file_single])




