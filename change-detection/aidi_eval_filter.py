import os
import sys
import shutil
import json
import random
sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *
import xml.dom.minidom

def parse_xml(xml_file):
	dom = xml.dom.minidom.parse(xml_file)
	root = dom.documentElement
	defect_num = root.getElementsByTagName('DefectNum')[0].childNodes[0].data
	list_0 = []
	list_1 = []
	list_2 = []
	list_3 = []
	for index in range(int(defect_num)):
		name = 'Defect' + str(index)
		defect_name_level = root.getElementsByTagName(name)[0].childNodes[0].data
		defect_name = defect_name_level.strip().split('-')[0]
		defect_level = defect_name_level.strip().split('-')[1]
		if defect_level == '放行':
			list_0.append(defect_name)
		elif defect_level == '轻度':
			list_1.append(defect_name)
		elif defect_level == '中度':
			list_2.append(defect_name)
		else:
			list_3.append(defect_name)
	return list_0,list_1,list_2,list_3


def get_name_score(one_label_path):
	in_label = LabelIO()
	in_label.read_from(one_label_path)
	json_label = json.loads(in_label.to_json())
	return json_label['regions'][0]['name'],json_label['regions'][0]['score']


def eval_one_set(root_dir,train_list):
	test_result_dir = root_dir + '/test_result'
	label_dir = root_dir + '/label'
	miss_dict = {}
	miss_list = []
	miss_num = 0

	over_list = []
	over_dict = {}
	over_num = 0
	total_num = 0.
	true_num = 0.
	for one_label in train_list:
		one_label_path = label_dir + '/' + one_label
		one_res_path = test_result_dir + '/' + one_label
		label_name,label_score = get_name_score(one_label_path)
		res_name,res_score = get_name_score(one_res_path)
		if res_name == 'OK' and label_name != 'OK': #漏检
			if label_name not in miss_list:
				miss_list.append(label_name)
				miss_dict[label_name] = 1
			else:
				miss_dict[label_name] += 1
			miss_num += 1
		if label_name == 'OK' and res_name != 'OK':
			if res_name not in over_list:
				over_list.append(res_name)
				over_dict[res_name] = 1
			else:
				over_dict[res_name] += 1
			over_num += 1
		total_num += 1
		if res_name == label_name:
			true_num += 1
	if total_num == 0:
		acc = 0
	else:
		acc = true_num/total_num
	print('漏检:\n',miss_dict,'总数： ',miss_num)
	print('过检:\n',over_dict,'总数： ',over_num)
	print('acc:\n',acc)


list_0_ = []
list_1_ = []
list_2_ = []
list_3_ = []
new_type = []

def init_list(xml_file):
	global list_0_,list_1_,list_2_,list_3_
	list_0_,list_1_,list_2_,list_3_ = parse_xml(xml_file)


def check_name_score(res_name,res_score):
	ok = 0
	ng = 1
	err = 2
	if res_name == 'OK':
		return ok

	if res_name in list_0_:
		return ok
	elif res_name in list_1_:
		return ng
	elif res_name in list_2_:
		if res_score < 0.45:
			return ok
		else:
			return ng
	elif res_name in list_3_:
		if res_score < 0.75:
			return ok
		else:
			return ng
	else:
		if res_name not in new_type:
			print('new defect type:  ',res_name)
			new_type.append(res_name)
		return err



def eval_one_filter(root_dir,train_list):
	test_result_dir = root_dir + '/test_result'
	label_dir = root_dir + '/label'
	miss_dict = {}
	miss_list = []
	miss_num = 0

	over_list = []
	over_dict = {}
	over_num = 0
	total_num = 0.
	true_num = 0.
	for one_label in train_list:
		one_label_path = label_dir + '/' + one_label
		one_res_path = test_result_dir + '/' + one_label
		label_name,label_score = get_name_score(one_label_path)
		res_name,res_score = get_name_score(one_res_path)

		flag_label = check_name_score(label_name,label_score)
		flag_res = check_name_score(res_name,res_score)

		if flag_label == 2 or flag_res == 2:
			continue

		if flag_label == 0 and flag_res == 1: #过检
			if res_name not in over_list:
				over_list.append(res_name)
				over_dict[res_name] = 1
			else:
				over_dict[res_name] += 1
			over_num += 1
		elif flag_label == 1 and flag_res == 0: #漏检
			if label_name not in miss_list:
				miss_list.append(label_name)
				miss_dict[label_name] = 1
			else:
				miss_dict[label_name] += 1
			miss_num += 1
		else:
			true_num += 1

		total_num += 1
	if total_num == 0:
		acc = 0
	else:
		acc = true_num/total_num
	print('漏检:\n',miss_dict,'总数： ',miss_num)
	print('过检:\n',over_dict,'总数： ',over_num)
	print('acc:\n',acc)



def eval_aidi_filter(root_dir,train_list,xml_file):
	init_list(xml_file)
	train_set = []
	test_set = []
	for one_label in os.listdir(root_dir + '/label'):
		index = one_label.strip().split('.')[0]
		if int(index) in train_list:
			train_set.append(one_label)
			train_list.remove(int(index))
		else:
			test_set.append(one_label)

	print('train results:      \n')	
	eval_one_filter(root_dir,train_set)
	print('test results:      \n')
	eval_one_filter(root_dir,test_set)



def eval_aidi_project(root_dir,train_list):
	train_set = []
	test_set = []
	for one_label in os.listdir(root_dir + '/label'):
		index = one_label.strip().split('.')[0]
		if int(index) in train_list:
			train_set.append(one_label)
			train_list.remove(int(index))
		else:
			test_set.append(one_label)

	print('train results:      \n')	
	eval_one_set(root_dir,train_set)
	print('test results:      \n')
	eval_one_set(root_dir,test_set)


def get_train_list(json_file):

	json_str = open(os.path.join(json_file),'r', encoding='UTF-8')
	json_dict = json.load(json_str)
	train_list = json_dict['indexes']['value']
	return train_list
	
if __name__ == '__main__':
	# root_dir = 'D:/yang.xie/aidi_projects/update-label0918/reg_cls_all/RegClassify_0'
	# json_file = root_dir + '/task.json'
	# train_list = get_train_list(json_file)
	# eval_aidi_project(root_dir,train_list)

	root_dir = 'D:/yang.xie/aidi_projects/update-label0918/reg_cls_all/RegClassify_0'
	json_file = root_dir + '/task.json'
	train_list = get_train_list(json_file)
	xml_file = 'D:/yang.xie/workspace/defects.xml'
	eval_aidi_filter(root_dir,train_list,xml_file)




	





					



