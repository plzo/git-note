import os
import sys
import shutil
import json
import random
import copy
import xlwt
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

def check_label_score(label_name,label_score):
	if label_name == 'OK':
		return True
	try:
		if label_score < xml_leval_dict_[label_name]:
			return True
		else:
			return False
	except:
		print('new defects type: ',label_name)



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


def make_pair(label_name,label_score):
	one_data = {}
	one_data['name'] = label_name
	one_data['score'] = label_score
	return one_data


def init_matrix(name_list):
	label_prob_dict = {}
	for name_row in name_list:
		tmp_dict = {}
		for name_col in name_list:
			tmp_dict[name_col] = 0.
		label_prob_dict[name_row] = tmp_dict
	return label_prob_dict


def matrix_reduce_0(matrix):
	matrix_reduce = {}
	for (name1, dict_tmp) in matrix.items():
		total = 0
		for (name2, num) in dict_tmp.items():
			total += num
		matrix_reduce[name1] = total
	return matrix_reduce

def get_eval_ng_ok(label_prob_matrix, name_list):
	total_sum = 0
	ng_true = 0
	ok_sum = 0
	ok_true = 0
	for one_name_row in name_list:
		for one_name_col in name_list:
			total_sum += label_prob_matrix[one_name_row][one_name_col]
			if one_name_row == one_name_col:
				if one_name_row == 'OK':
					ok_true = label_prob_matrix[one_name_row][one_name_col]
				else:
					ng_true += label_prob_matrix[one_name_row][one_name_col]
			if one_name_row == 'OK':
				ok_sum += label_prob_matrix[one_name_row][one_name_col]
	res = {}
	res['ok_recall'] = ok_true / ok_sum
	res['ng_recall'] = ng_true / (total_sum - ok_sum)
	return res
		

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
	origin_matrix = init_matrix(name_list)
	label_prob_matrix = copy.deepcopy(origin_matrix)
	prob_label_matrix = copy.deepcopy(origin_matrix)

	for i in range(len(label_list)):
		label_prob_matrix[label_list[i]['name']][prob_list[i]['name']] += 1
		prob_label_matrix[prob_list[i]['name']][label_list[i]['name']] += 1

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

	for num,one_name in enumerate(name_list):
		train_sheet.write(0,num + 1,one_name)
		train_sheet.write(num + 1,0,one_name)
	for row,row_name in enumerate(name_list):
		for col,col_name in enumerate(name_list):
			if row == col:
				train_sheet.write(row + 1,col + 1,label_prob_matrix[row_name][col_name], style_green)
			elif label_prob_matrix[row_name][col_name] > 0:
				train_sheet.write(row + 1,col + 1,label_prob_matrix[row_name][col_name], style_red)
			else:
				train_sheet.write(row + 1,col + 1,label_prob_matrix[row_name][col_name])
	
	eval_dict = get_eval_ng_ok(label_prob_matrix, name_list)

	col_num = len(name_list)
	col_num += 1
	train_sheet.write(col_num, 0, 'ok_recall')
	train_sheet.write(col_num, 1, eval_dict['ok_recall'])
	train_sheet.write(col_num + 1, 0, 'ng_recall')
	train_sheet.write(col_num + 1, 1, eval_dict['ng_recall'])

	row_num = len(name_list)
	row_num += 1
	train_sheet.write(0,row_num,'defects_name')
	for num,one_name in enumerate(name_list):	
		train_sheet.write(num + 1,row_num,one_name)

	row_num += 1
	# train_sheet.write(row_num,0,'precision')
	train_sheet.write(0,row_num,'recall')
	train_sheet.write(0,row_num + 1,'precision')

	label_prob_matrix_reduce = matrix_reduce_0(label_prob_matrix)
	prob_label_matrix_reduce = matrix_reduce_0(prob_label_matrix)

	for num,one_name in enumerate(name_list):
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
	train_sheet.write(0,row_num,'total_num')
	for num,one_name in enumerate(name_list):	
		train_sheet.write(num + 1,row_num,label_prob_matrix_reduce[one_name])
	
	workbook.save(out_path)



def eval_confusion_matrix(root_dir,json_file,out_path):
	train_list = get_train_list(json_file)
	train_set,test_set = get_set(root_dir, train_list)

	get_matrix(root_dir,train_set,out_path + '_train.xlsx')
	get_matrix(root_dir,test_set,out_path + '_test.xlsx')



	
if __name__ == '__main__':

	# out_path = 'D:/yang.xie/data/数据分析/classify_score0.9'
	# root_dir_all = 'D:/yang.xie/aidi_projects/project-20201022/classify_score0.9/RegClassify_0'

	out_path = 'D:/yang.xie/data/数据分析/classify_no_reg'
	root_dir_all = 'D:/yang.xie/aidi_projects/project-20201022/classify_no_reg/Classify_0'

	json_file_all = root_dir_all + '/task.json'
	# xml_file = root_dir_all + '/defects_filter.xml'

	eval_confusion_matrix(root_dir_all,json_file_all,out_path)








