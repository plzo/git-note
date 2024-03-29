import os
import sys
import shutil
import json
import random
import copy
import xlwt
import sqlite3
from xlwt import *
sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *
import xml.dom.minidom

xml_leval_dict_ = {}
# confusion_matrix_dict_ = {}

def get_name_score(one_label_path):
	in_label = LabelIO()
	in_label.read_from(one_label_path)
	tmp = in_label.to_json()
	json_label = json.loads(tmp)
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

def parse_xml(xml_file):
	dom = xml.dom.minidom.parse(xml_file)
	root = dom.documentElement
	defect_num = root.getElementsByTagName('DefectNum')[0].childNodes[0].data
	xml_leval_dict = {}
	for index in range(int(defect_num)):
		name = 'Defect' + str(index)
		defect_name_level = root.getElementsByTagName(name)[0].childNodes[0].data
		defect_name = defect_name_level.strip().split('-')[0]
		defect_level = defect_name_level.strip().split('-')[1]
		if defect_level == '放行':
			xml_leval_dict[defect_name] = 9.
		elif defect_level == '严重':
			xml_leval_dict[defect_name] = 0.75
		elif defect_level == '中度':
			xml_leval_dict[defect_name] = 0.45
		else:
			xml_leval_dict[defect_name] = -9.
	return xml_leval_dict

class_type = []
def check_label_score(label_name,label_score):
	if label_name == 'OK':
		return True
	try:
		if label_score < xml_leval_dict_[label_name]:
			return True
		else:
			return False
	except:
		global class_type
		if label_name not in class_type:
			class_type.append(label_name)
			print('new defects type: ',label_name)
		return True

def compare_label_small(label_pair,prob_pair):	
	res1 = ''
	if len(xml_leval_dict_) > 0:
		res_label = check_label_score(label_pair['name'],label_pair['score'])
		res_prob = check_label_score(prob_pair['name'],prob_pair['score'])
		if res_label and res_prob:
			res1 = 'ok_ok'
		elif res_label and not res_prob:
			res1 = 'ok_ng'
		elif res_prob and not res_label:
			res1 = 'ng_ok'
		else:
			res1 = 'ng_ng'
	return res1

def compare_label(label_path,prob_path):
	label_name,label_score = get_name_score(label_path)
	prob_name,prob_score = get_name_score(prob_path)	
	res1 = ''
	res2 = ''
	if len(xml_leval_dict_) > 0:
		res_label = check_label_score(label_name,label_score)
		res_prob = check_label_score(prob_name,prob_score)
		if res_label and res_prob:
			res1 = 'ok_ok'
		elif res_label and not res_prob:
			res1 = 'ok_ng'
		elif res_prob and not res_label:
			res1 = 'ng_ok'
		else:
			res1 = 'ng_ng'

	if label_name == 'OK' and prob_name == 'OK':
		res2 = 'ok_true'
	elif label_name == 'OK' and prob_name != 'OK':
		res2 = 'ok_over'
	elif label_name != 'OK' and prob_name == 'OK':
		res2 = 'ok_miss'
	else:
		if get_level(label_score) > get_level(prob_score):
			if label_name == prob_name:
				res2 = 'ng_miss_same'
			else:
				res2 = 'ng_miss_diff'
		elif get_level(prob_score) > get_level(label_score):
			if label_name == prob_name:
				res2 = 'ng_over_same'
			else:
				res2 = 'ng_over_diff'
		else:
			if label_name == prob_name:
				res2 = 'same_true'
			else:
				res2 = 'diff_true'
	return res1,res2

def get_set(root_dir, train_list):
	train_set = []
	test_set = []
	print(root_dir)
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
	compare_res = {'ok_ok': 0., 'ok_ng': 0., 'ng_ok': 0., 'ng_ng': 0., 'ok_true': 0., 'same_true': 0., 'diff_true': 0., 'ok_miss': 0., 'ng_miss_same': 0., 'ng_miss_diff': 0., 'ok_over': 0., 'ng_over_same': 0., 'ng_over_diff': 0.}
	for one_label in train_list:
		label_path = label_dir + '/' + one_label
		prob_path = test_result_dir + '/' + one_label
		if len(xml_leval_dict_) > 0:
			compare_res[compare_label(label_path,prob_path)[0]] += 1
		compare_res[compare_label(label_path,prob_path)[1]] += 1
	return compare_res

def make_pair(label_name,label_score):
	one_data = {}
	one_data['name'] = label_name
	one_data['score'] = label_score
	return one_data


def list_add_level(name_list):
	name_list_level = []
	for name in name_list:
		if name == 'OK':
			name_list_level.append(name)
			continue
		name_list_level.append(name + '_轻度')
		name_list_level.append(name + '_中度')
		name_list_level.append(name + '_严重')
	return name_list_level


def init_matrix(name_list):
	label_prob_dict = {}
	for name_row in name_list:
		tmp_dict = {}
		for name_col in name_list:
			tmp_dict[name_col] = 0.
		label_prob_dict[name_row] = tmp_dict
	return label_prob_dict

def get_name_level(one_data):
	if one_data['name'] == 'OK':
		return 'OK'
	if one_data['score'] < 0.45:
		return one_data['name'] + '_轻度'
	if one_data['score'] < 0.75:
		return one_data['name'] + '_中度'
	return one_data['name'] + '_严重'

def matrix_reduce_0(matrix):
	matrix_reduce = {}
	for (name1, dict_tmp) in matrix.items():
		total = 0
		for (name2, num) in dict_tmp.items():
			total += num
		matrix_reduce[name1] = total
	return matrix_reduce
		

def get_matrix(root_dir,train_list,out_path):
	name_dict = {}
	name_list = []
	label_list = []
	prob_list = []

	test_result_dir = root_dir + '/test_result'
	label_dir = root_dir + '/label'
	for one_label in train_list:
		label_path = label_dir + '/' + one_label
		prob_path = test_result_dir + '/' + one_label
		label_name,label_score = get_name_score(label_path)
		prob_name,prob_score = get_name_score(prob_path)

		name_dict[label_name] = 0
		name_dict[prob_name] = 0

		label_list.append(make_pair(label_name,label_score))
		prob_list.append(make_pair(prob_name,prob_score))
	for (name,num) in name_dict.items():
		name_list.append(name)

	name_list = sorted(name_list)	
	name_list_level = list_add_level(name_list)
	origin_matrix = init_matrix(name_list_level)
	origin_matrix_small = init_matrix(name_list)

	label_dict = {}
	for name in name_list:
		label_dict[name] = 0

	label_prob_matrix = copy.deepcopy(origin_matrix)
	prob_label_matrix = copy.deepcopy(origin_matrix)

	label_prob_matrix_small = copy.deepcopy(origin_matrix_small)
	prob_label_matrix_small = copy.deepcopy(origin_matrix_small)
	for i in range(len(label_list)):
		new_label_name = get_name_level(label_list[i])
		new_prob_name = get_name_level(prob_list[i])
		label_prob_matrix[new_label_name][new_prob_name] += 1
		prob_label_matrix[new_prob_name][new_label_name] += 1

		label_prob_matrix_small[label_list[i]['name']][prob_list[i]['name']] += 1
		prob_label_matrix_small[prob_list[i]['name']][label_list[i]['name']] += 1

		if compare_label_small(label_list[i],prob_list[i]) == 'ng_ok':
			label_dict[label_list[i]['name']] += 1

	workbook = xlwt.Workbook(encoding='utf-8')
	train_sheet = workbook.add_sheet('sheet 1', cell_overwrite_ok=True)	


	style_green = XFStyle()
	pattern = Pattern()
	pattern.pattern = Pattern.SOLID_PATTERN
	pattern.pattern_fore_colour = Style.colour_map['light_green'] 
	style_green.pattern = pattern

	style_red = XFStyle()
	pattern = Pattern()
	pattern.pattern = Pattern.SOLID_PATTERN
	pattern.pattern_fore_colour = Style.colour_map['rose'] 
	style_red.pattern = pattern

	for num,one_name in enumerate(name_list_level):
		train_sheet.write(0,num + 1,one_name)
		train_sheet.write(num + 1,0,one_name)
	for row,row_name in enumerate(name_list_level):
		for col,col_name in enumerate(name_list_level):
			if row == col:
				train_sheet.write(row + 1,col + 1,label_prob_matrix[row_name][col_name], style_green)
			elif label_prob_matrix[row_name][col_name] > 0:
				train_sheet.write(row + 1,col + 1,label_prob_matrix[row_name][col_name], style_red)
			else:
				train_sheet.write(row + 1,col + 1,label_prob_matrix[row_name][col_name])

	row_num = len(name_list_level)
	row_num += 1
	train_sheet.write(0,row_num,'defects_name')
	for num,one_name in enumerate(name_list_level):	
		train_sheet.write(num + 1,row_num,one_name)

	row_num += 1
	# train_sheet.write(row_num,0,'precision')
	train_sheet.write(0,row_num,'recall')
	train_sheet.write(0,row_num + 1,'precision')

	label_prob_matrix_reduce = matrix_reduce_0(label_prob_matrix)
	prob_label_matrix_reduce = matrix_reduce_0(prob_label_matrix)

	label_prob_matrix_small_reduce = matrix_reduce_0(label_prob_matrix_small)
	prob_label_matrix_small_reduce = matrix_reduce_0(prob_label_matrix_small)

	for num,one_name in enumerate(name_list_level):
		if label_prob_matrix_reduce[one_name] == 0:
			recall = -1
		else:
			recall = label_prob_matrix[one_name][one_name] / label_prob_matrix_reduce[one_name]
		if prob_label_matrix_reduce[one_name] == 0:
			precision = -1
		else:
			precision = label_prob_matrix[one_name][one_name] / prob_label_matrix_reduce[one_name]
		train_sheet.write(num + 1,row_num,recall)
		train_sheet.write(num + 1,row_num + 1,precision)
		# train_sheet.write(row_num,num + 1,precision)
	
	row_num += 2
	# train_sheet.write(row_num,0,'precision_sum')
	train_sheet.write(0,row_num,'recall_sum')
	train_sheet.write(0,row_num + 1,'precision_sum')
	count = 0
	for num,one_name in enumerate(name_list):
		if label_prob_matrix_small_reduce[one_name] == 0:
			recall = -1
		else:
			recall = label_prob_matrix_small[one_name][one_name] / label_prob_matrix_small_reduce[one_name]
		if prob_label_matrix_small_reduce[one_name] == 0:
			precision = -1
		else:
			precision = label_prob_matrix_small[one_name][one_name] / prob_label_matrix_small_reduce[one_name]
		if one_name == 'OK':
			train_sheet.write(count + 1,row_num,recall)
			train_sheet.write(count + 1,row_num + 1,precision)
			count += 1
			continue

		train_sheet.write(count + 1,row_num,recall)
		train_sheet.write(count + 2,row_num,recall)
		train_sheet.write(count + 3,row_num,recall)
		train_sheet.write(count + 1,row_num + 1,precision)
		train_sheet.write(count + 2,row_num + 1,precision)
		train_sheet.write(count + 3,row_num + 1,precision)
		count += 3
		# train_sheet.write(row_num,num * 3 + 1,precision)

	row_num += 2
	train_sheet.write(0,row_num,'total_num')
	for num,one_name in enumerate(name_list_level):	
		train_sheet.write(num + 1,row_num,label_prob_matrix_reduce[one_name])

	row_num += 1
	train_sheet.write(0,row_num,'total_num_sum')
	count = 0
	for num,one_name in enumerate(name_list):
		if one_name == 'OK':
			train_sheet.write(count + 1,row_num,label_prob_matrix_small_reduce[one_name])
			count += 1
			continue	
		train_sheet.write(count + 1,row_num,label_prob_matrix_small_reduce[one_name])
		train_sheet.write(count + 2,row_num,label_prob_matrix_small_reduce[one_name])
		train_sheet.write(count + 3,row_num,label_prob_matrix_small_reduce[one_name])
		count += 3

	row_num += 1
	train_sheet.write(0,row_num,'miss_num_sum')
	count = 0
	for num,one_name in enumerate(name_list):
		if one_name == 'OK':
			train_sheet.write(count + 1,row_num,label_dict[one_name])
			count += 1
			continue	
		train_sheet.write(count + 1,row_num,label_dict[one_name])
		train_sheet.write(count + 2,row_num,label_dict[one_name])
		train_sheet.write(count + 3,row_num,label_dict[one_name])
		count += 3

	miss_rate = {}
	for name in name_list:
		if label_prob_matrix_small_reduce[name] == 0:
			miss_rate[name] = 0
		else:
			miss_rate[name] = label_dict[name]/label_prob_matrix_small_reduce[name]
	
	row_num += 1
	train_sheet.write(0,row_num,'miss_rate')
	count = 0
	for num,one_name in enumerate(name_list):
		if one_name == 'OK':
			train_sheet.write(count + 1,row_num,miss_rate[one_name])
			count += 1
			continue	
		train_sheet.write(count + 1,row_num,miss_rate[one_name])
		train_sheet.write(count + 2,row_num,miss_rate[one_name])
		train_sheet.write(count + 3,row_num,miss_rate[one_name])
		count += 3
	
	workbook.save(out_path)

	# return label_list,prob_list,name_list


def eval_confusion_matrix(root_dir,json_file,out_path,xml_file = ''):
	global xml_leval_dict_
	if xml_file != '':
		xml_leval_dict_ = parse_xml(xml_file)
	train_list = get_train_list(json_file)
	train_set,test_set = get_set(root_dir, train_list)

	get_matrix(root_dir,train_set,out_path + '_train.xlsx')
	get_matrix(root_dir,test_set,out_path + '_test.xlsx')



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


workbook_global_ = xlwt.Workbook(encoding='utf-8')
sheet_global_ = workbook_global_.add_sheet('sheet 1', cell_overwrite_ok=True)
row_num_ = 0

def eval_display(compare_res):
	total_num = 0.
	for (name,num) in compare_res.items():
		if not (name == 'ok_ok' or name == 'ok_ng' or name == 'ng_ok' or name == 'ng_ng'):
			total_num += num
	global workbook_global_
	global sheet_global_
	global row_num_

	count_tmp = 0
	for (name, num) in compare_res.items():
		sheet_global_.write(row_num_,count_tmp,name)
		sheet_global_.write(row_num_ + 1,count_tmp,num)
		count_tmp += 1
	row_num_ += 3

	print('中间结果：\n',compare_res)
	print('*********程度相等 = true，计算指标************')
	# miss = (compare_res['ok_miss'] + compare_res['ng_miss_same'] + compare_res['ng_miss_diff']) / total_num
	# over = (compare_res['ok_over'] + compare_res['ng_over_same'] + compare_res['ng_over_diff']) / total_num
	# acc = (compare_res['ok_true'] + compare_res['same_true'] + compare_res['diff_true']) / total_num
	# print('漏检率:\n',miss * 100)
	# print('过检率:\n',over * 100)
	# print('acc:\n',acc * 100)
	if (total_num - compare_res['ok_true'] - compare_res['ok_over']) == 0:
		defect_rc_1 = 0
	else:
		defect_rc_1 = (compare_res['diff_true'] + compare_res['same_true']) / (total_num - compare_res['ok_true'] - compare_res['ok_over'])


	if (compare_res['ok_over'] + compare_res['diff_true'] + compare_res['same_true']) == 0:
		defect_pr_1 = 0
	else:
		defect_pr_1 = (compare_res['diff_true'] + compare_res['same_true']) / (compare_res['ok_over'] + compare_res['diff_true'] + compare_res['same_true'])
	
	print('defect_rc_1:\n',defect_rc_1 * 100)
	print('defect_pr_1:\n',defect_pr_1 * 100)

	if (compare_res['diff_true'] + compare_res['same_true']) == 0:
		mix = 0
	else:
		mix = compare_res['diff_true'] / (compare_res['diff_true'] + compare_res['same_true'])
	print('混淆率:\n',mix * 100)

	print('*********类型一致 = true，计算指标************')

	if (total_num - compare_res['ok_true'] - compare_res['ok_over']) == 0:
		defect_rc_2 = 0
	else:
		defect_rc_2 = (compare_res['ng_miss_same'] + compare_res['ng_over_same'] + compare_res['same_true']) / (total_num - compare_res['ok_true'] - compare_res['ok_over'])
	
	if (compare_res['ok_over'] + compare_res['ng_miss_diff'] + compare_res['ng_over_diff'] + compare_res['diff_true'] + compare_res['ng_miss_same'] + compare_res['ng_over_same'] + compare_res['same_true']) == 0:
		defect_pr_2 = 0
	else:
		defect_pr_2 = (compare_res['ng_miss_same'] + compare_res['ng_over_same'] + compare_res['same_true']) / (compare_res['ok_over'] + compare_res['ng_miss_diff'] + compare_res['ng_over_diff'] + compare_res['diff_true'] + compare_res['ng_miss_same'] + compare_res['ng_over_same'] + compare_res['same_true'])
	
	print('defect_rc_2:\n',defect_rc_2 * 100)
	print('defect_pr_2:\n',defect_pr_2 * 100)


	print('*********程度相等 且 类型一致 = true，计算指标************')

	if (total_num - compare_res['ok_true'] - compare_res['ok_over']) == 0:
		defect_rc_3 = 0
	else:
		defect_rc_3 = compare_res['same_true'] / (total_num - compare_res['ok_true'] - compare_res['ok_over'])
	

	if (compare_res['ok_over'] + compare_res['diff_true'] + compare_res['same_true']) == 0:
		defect_pr_3 = 0
	else:
		defect_pr_3 = compare_res['same_true'] / (compare_res['ok_over'] + compare_res['diff_true'] + compare_res['same_true'])
	
	print('defect_rc_3:\n',defect_rc_3 * 100)
	print('defect_pr_3:\n',defect_pr_3 * 100)

	print('*********其他**********')

	if total_num == 0:
		aidi_acc = 0
	else:
		aidi_acc = (compare_res['ok_true'] + compare_res['same_true'] + compare_res['ng_miss_same'] + compare_res['ng_over_same']) / total_num
	
	print('aidi_acc:\n',aidi_acc * 100)
	print('total_num:\n',total_num)


	sheet_global_.write(row_num_,0,'程度召回')
	sheet_global_.write(row_num_ + 1,0,defect_rc_1)

	sheet_global_.write(row_num_,1,'程度精度')
	sheet_global_.write(row_num_ + 1,1,defect_pr_1)

	sheet_global_.write(row_num_,2,'类型召回')
	sheet_global_.write(row_num_ + 1,2,defect_rc_2)

	sheet_global_.write(row_num_,3,'类型精度')
	sheet_global_.write(row_num_ + 1,3,defect_pr_2)

	sheet_global_.write(row_num_,4,'程度类型召回')
	sheet_global_.write(row_num_ + 1,4,defect_rc_3)

	sheet_global_.write(row_num_,5,'程度类型精度')
	sheet_global_.write(row_num_ + 1,5,defect_pr_3)

	sheet_global_.write(row_num_,6,'混淆率')
	sheet_global_.write(row_num_ + 1,6,mix)

	sheet_global_.write(row_num_,7,'aidi指标')
	sheet_global_.write(row_num_ + 1,7,aidi_acc)

	sheet_global_.write(row_num_,8,'总数据量')
	sheet_global_.write(row_num_ + 1,8,total_num)
	
	if len(xml_leval_dict_) > 0:
		print('*********现场标准，计算指标************')
		defects_rc = compare_res['ng_ng'] / (compare_res['ng_ng'] + compare_res['ng_ok'])
		defects_pr = compare_res['ng_ng'] / (compare_res['ng_ng'] + compare_res['ok_ng'])
		ok_rc = compare_res['ok_ok'] / (compare_res['ok_ok'] + compare_res['ok_ng'])
		ok_pr = compare_res['ok_ok'] / (compare_res['ok_ok'] + compare_res['ng_ok'])
		ng_origin = total_num - compare_res['ok_true'] - compare_res['ok_over']
		ng_filter = compare_res['ng_ng'] + compare_res['ng_ok']
		print('defects_rc:\n',defects_rc)
		print('defects_pr:\n',defects_pr)
		print('ok_rc:\n',ok_rc)
		print('ok_pr:\n',ok_pr)
		print('ng_origin: ',ng_origin,'ng_filter: ',ng_filter)

		sheet_global_.write(row_num_,9,'现场缺陷召回')
		sheet_global_.write(row_num_ + 1,9,defects_rc)

		sheet_global_.write(row_num_,10,'现场缺陷精度')
		sheet_global_.write(row_num_ + 1,10,defects_pr)

		sheet_global_.write(row_num_,11,'现场ok召回')
		sheet_global_.write(row_num_ + 1,11,ok_rc)

		sheet_global_.write(row_num_,12,'现场ok精度')
		sheet_global_.write(row_num_ + 1,12,ok_pr)

		sheet_global_.write(row_num_,13,'现场缺陷原始数')
		sheet_global_.write(row_num_ + 1,13,ng_origin)

		sheet_global_.write(row_num_,14,'现场缺陷过滤数')
		sheet_global_.write(row_num_ + 1,14,ng_filter)
	row_num_ += 3

def eval_level_mixrate(root_dir_list,json_file_list,out_path,xml_file = ''):
	if len(root_dir_list) != len(json_file_list):
		return
	global xml_leval_dict_
	if xml_file != '':
		xml_leval_dict_ = parse_xml(xml_file)
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
	global workbook_global_
	workbook_global_.save(out_path + '_eval.xlsx')


# def append_dict(str1,str2):
# 	global confusion_matrix_dict_
# 	try:
# 		confusion_matrix_dict_[str1][str2] += 1
# 	except:
# 		try:
# 			confusion_matrix_dict_[str1][str2] = 1
# 		except:
# 			confusion_matrix_dict_[str1] = {}
# 			confusion_matrix_dict_[str1][str2] = 1
# 	try:
# 		confusion_matrix_dict_[str2][str1] += 0
# 	except:
# 		try:
# 			confusion_matrix_dict_[str2][str1] = 0
# 		except:
# 			confusion_matrix_dict_[str2] = {}
# 			confusion_matrix_dict_[str2][str1] = 0		

	
if __name__ == '__main__':
	# project_name = 'reg_cls_tmp2'
	# root_dir_all = 'D:/yang.xie/aidi_projects/update-label0918/'+ project_name + '/RegClassify_0'

	# project_name = 'classify_410'
	# root_dir_all = 'D:/yang.xie/aidi_tasks/classify_410'
	# json_file_all = root_dir_all + '/task.json'

	# root_dir_double = 'D:/yang.xie/aidi_projects/update-label0918/reg_cls_double/RegClassify_0'
	# json_file_double = root_dir_double + '/task.json'
	# root_dir_single = 'D:/yang.xie/aidi_projects/update-label0918/reg_cls_single/RegClassify_0'
	# json_file_single = root_dir_single + '/task.json'

	# print('********************reg_cls_all*********************')
	# eval_level_mixrate([root_dir_all],[json_file_all])
	# print('********************reg_cls_double*********************')
	# eval_level_mixrate([root_dir_double],[json_file_double])
	# print('********************reg_cls_single*********************')
	# eval_level_mixrate([root_dir_single],[json_file_single])
	# print('********************reg_cls_double single*********************')
	# eval_level_mixrate([root_dir_double,root_dir_single],[json_file_double,json_file_single])


	# out_path = 'D:/yang.xie/data/数据分析/5_cls'
	# root_dir_all = 'D:/yang.xie/aidi_projects/project-20201022/5_cls/RegClassify_0'

	# out_path = 'D:/yang.xie/data/数据分析/cls-seg-v1-seg2'
	# root_dir_all = 'D:/yang.xie/aidi_projects/cls-seg20201027/base_project_copy/RegClassify_0'	
	# xml_file = root_dir_all + '/defects_filter.xml'

	# out_path = 'D:/yang.xie/data/数据分析/shennan_cls'
	# root_dir_all = 'D:/yang.xie/aidi_projects/shennan1107/1105-2C/RegClassify_0'	
	# xml_file = ''

	# out_path = 'D:/yang.xie/data/数据分析/shennan_cls_seg_reset_v0'
	# root_dir_all = 'D:/yang.xie/aidi_projects/shennan1107/seg_cls/RegClassify_0'	
	# xml_file = ''


	# out_path = 'D:/yang.xie/data/数据分析/base_project_develop_v2'
	# root_dir_all = 'D:/yang.xie/aidi_projects/project-20201022/base_project/RegClassify_0'	
	# xml_file = root_dir_all + '/defects_filter.xml'

	out_path = 'D:/yang.xie/data/数据分析/iter04_v1'
	root_dir_all = 'D:/yang.xie/aidi_projects/20201117-iteration4/iter04/RegClassify_0'	
	xml_file = root_dir_all + '/defects_filter.xml'
	
	

	json_file_all = root_dir_all + '/task.json'
	eval_confusion_matrix(root_dir_all,json_file_all,out_path,xml_file)
	print('start eval_level_mixrate... ')
	eval_level_mixrate([root_dir_all],[json_file_all],out_path,xml_file)

	# print(get_train_list(r'D:\yang.xie\aidi_projects\20201117-iteration4\channel3\channel3.db'))







