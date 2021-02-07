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

class xlwt_tools():
	def __init__(self,out_path):
		self.workbook = xlwt.Workbook(encoding ='utf-8')
		self.sheets = {}
		self.out_path = out_path
	def add_sheet(self, sheet_name):
		self.sheets[sheet_name] = self.workbook.add_sheet(sheet_name, cell_overwrite_ok = True)
	
	def get_sheet(self, sheet_name):
		for (name,sheet) in self.sheets.items():
			if name == sheet_name:
				return sheet
		self.add_sheet(sheet_name)
		return self.sheets[sheet_name]

	def get_style(self,color):
		style = XFStyle()
		pattern = Pattern()
		pattern.pattern = Pattern.SOLID_PATTERN
		pattern.pattern_fore_colour = Style.colour_map[color] 
		style.pattern = pattern
		return style
	
	def draw_matrix(self, sheet_name, base_row, base_col, matrix_dict, name_list):
		# for (class_name,sub_dict) in matrix_dict.items():
		# 	name_list.append(class_name)
		# name_list = sorted(name_list)

		sheet = self.get_sheet(sheet_name)
		style_green = self.get_style('light_green')
		style_red = self.get_style('rose')

		# for num,one_name in enumerate(name_list):
		# 	sheet.write(base_row, base_col + num + 1,one_name)
		# 	sheet.write(base_row + num + 1, base_col, one_name)

		self.draw_row(sheet_name, base_row, base_col + 1,name_list)
		self.draw_col(sheet_name, base_row + 1, base_col,name_list)

		for row, row_name in enumerate(name_list):
			for col, col_name in enumerate(name_list):
				if row == col:
					sheet.write(base_row + row + 1,base_col + col + 1, matrix_dict[row_name][col_name], style_green)
				elif matrix_dict[row_name][col_name] > 0:
					sheet.write(base_row + row + 1,base_col + col + 1, matrix_dict[row_name][col_name], style_red)
				else:
					sheet.write(base_row + row + 1,base_col + col + 1, matrix_dict[row_name][col_name])

	def draw_col(self, sheet_name, base_row, base_col, col_list):
		sheet = self.get_sheet(sheet_name)
		for num,one_name in enumerate(col_list):
			sheet.write(base_row + num, base_col, one_name)

	def draw_row(self, sheet_name, base_row, base_col, row_list):
		sheet = self.get_sheet(sheet_name)
		for num,one_name in enumerate(row_list):			
			sheet.write(base_row, base_col + num,one_name)

	def save(self):
		self.workbook.save(self.out_path)

class eval_tools():
	def __init__(self,root_dir, out_path):
		self.root_dir = root_dir
		self.eval_set = 'test'
		self.list_src = 'db'

		self.name_list = []
		self.name_level_list = []
		self.pair_list = []
		self.matrix = {}
		self.reduce_matrix_row = {}
		self.reduce_matrix_col = {}
		self.precision = []
		self.recall = []
		self.total_num = []
		self.miss_num = []

		self.add_level = False
		self.have_xml = False

		self.global_result = {}
		self.global_result_name = []
		self.global_result_value = []

		self.tool = xlwt_tools(out_path)
		self.xml_level_dict = self.init_xml_level()
		self.init_data()
	
	def set_add_level(self,add_level):
		self.add_level = add_level

	def init_xml_level(self):
		xml_path = self.get_xml_file()
		xml_level_dict = {}
		if xml_path != '':
			xml_level_dict = self.parse_xml(xml_path)
		return xml_level_dict
			
	def set_eval_set(self,eval_set):
		self.eval_set = eval_set
		self.init_data()
		

	def init_data(self):
		self.name_list, self.pair_list = self.get_name_score_list()
		self.name_list = sorted(self.name_list)
		self.name_level_list = self.list_add_level()
		self.global_result_name = []
		self.global_result_value = []

	def list_add_level(self):
		name_level_list = []
		for name in self.name_list:
			if name == 'OK':
				name_level_list.append(name)
				continue
			name_level_list.append(name + '_轻度')
			name_level_list.append(name + '_中度')
			name_level_list.append(name + '_严重')
		return name_level_list
		
	def get_db_file(self):
		for one_file in os.listdir(self.root_dir + '/..'):
			if one_file.endswith('.db'):
				return self.root_dir + '/../' + one_file
		print('Can not find db file!')
		return ''

	def get_xml_file(self):
		for one_file in os.listdir(self.root_dir):
			if one_file.endswith('.xml'):
				self.have_xml = True
				return self.root_dir + '/' + one_file
		print('Can not find xml file!')
		return ''

	def get_task_list(self):
		json_str = open(self.root_dir + '/task.json','r', encoding='UTF-8')
		json_dict = json.load(json_str)
		train_list = json_dict['indexes']['value']
		test_list = []
		if self.eval_set == 'train':
			self.set_list = train_list
		else:
			for one_label in os.listdir(root_dir + '/label'):
				index = int(one_label.strip().split('.')[0])
				if index not in train_list:
					test_list.append(index)
			self.set_list = test_list
			
	def get_list(self):
		db_file = self.get_db_file()			
		with sqlite3.connect(db_file) as conn:
			c = conn.cursor()
			if self.eval_set == 'train':
				try:
					cursor = c.execute("SELECT id FROM RegClassify_0 WHERE selected == 1")
				except:
					cursor = c.execute("SELECT id FROM Classify_0 WHERE selected == 1")
			else:
				try:
					cursor = c.execute("SELECT id FROM RegClassify_0 WHERE selected == 2")
				except:
					cursor = c.execute("SELECT id FROM Classify_0 WHERE selected == 2")
			self.set_list = [row[0] for row in cursor]

	def get_label_suffix(self):
		for one_label in os.listdir(self.root_dir + '/label'):
			if one_label.endswith('.aqlabel'):
				return '.aqlabel'
			elif one_label.endswith('.json'):
				return '.json'
		print('Label suffix error!')
		return ''

	def init_matrix(self,name_list):
		res_dict = {}
		for name_row in name_list:
			tmp_dict = {}
			for name_col in name_list:
				tmp_dict[name_col] = 0.
			res_dict[name_row] = tmp_dict
		return res_dict

	def get_result(self,tp = 'rc'):
		result = []
		if self.add_level:
			name_list = self.name_level_list
		else:
			name_list = self.name_list

		if tp == 'rc':
			reduce_matrix = self.reduce_matrix_row
		else:
			reduce_matrix = self.reduce_matrix_col
		for one_name in name_list:
			if reduce_matrix[one_name] > 0:
				result.append(self.matrix[one_name][one_name] / reduce_matrix[one_name])
			else:
				result.append(-1)
		return result
	
	def get_total_num(self):
		total = []
		if self.add_level:
			name_list = self.name_level_list
		else:
			name_list = self.name_list		
		for one_name in name_list:
			total.append(self.reduce_matrix_row[one_name])
		return total
	
	def get_miss_num(self):
		if not self.have_xml:
			return []
		miss_dict = {}
		for one_name in self.name_list:
			miss_dict[one_name] = 0
		for one_pair in self.pair_list:
			if one_pair['res_xml'] == 'ng_ok':
				miss_dict[one_pair['label']['name']] += 1
		miss_list = []
		for (name, num) in miss_dict.items():
			miss_list.append(num)
		return miss_list
	
	def compare(self):
		new_pair_list = []
		for one_pair in self.pair_list:
			if self.have_xml:
				one_pair['res_xml'] = self.compare_label_xml(one_pair['label'],one_pair['prob'])
			one_pair['res'] = self.compare_label(one_pair['label'],one_pair['prob'])
			new_pair_list.append(one_pair)
		self.pair_list = new_pair_list
		
	def parse_xml(self,xml_file):
		dom = xml.dom.minidom.parse(xml_file)
		root = dom.documentElement
		defect_num = root.getElementsByTagName('DefectNum')[0].childNodes[0].data
		xml_level_dict = {}
		for index in range(int(defect_num)):
			name = 'Defect' + str(index)
			defect_name_level = root.getElementsByTagName(name)[0].childNodes[0].data
			defect_name = defect_name_level.strip().split('-')[0]
			defect_level = defect_name_level.strip().split('-')[1]
			if defect_level == '放行':
				xml_level_dict[defect_name] = 9.
			elif defect_level == '严重':
				xml_level_dict[defect_name] = 0.75
			elif defect_level == '中度':
				xml_level_dict[defect_name] = 0.45
			else:
				xml_level_dict[defect_name] = -9.
		return xml_level_dict


	def check_label_score(self,label_name,label_score):
		if label_name == 'OK':
			return True
		try:
			if label_score < self.xml_level_dict[label_name]:
				return True
			else:
				return False
		except:
			# try:
			# 	if label_score < self.xml_level_dict[label_name.split('_')[0]]:
			# 		return True
			# 	else:
			# 		return False
			# except:
			if self.add_level:
				class_type = self.name_level_list
			else:
				class_type = self.name_list
			if label_name not in class_type:
				class_type.append(label_name)
				print('new defects type: ',label_name)
			return True

	def compare_label_xml(self,label_pair,prob_pair):	
		if not self.have_xml:
			return ''
		res_label = self.check_label_score(label_pair['name'],label_pair['score'])
		res_prob = self.check_label_score(prob_pair['name'],prob_pair['score'])
		if res_label and res_prob:
			return 'ok_ok'
		elif res_label and not res_prob:
			return 'ok_ng'
		elif res_prob and not res_label:
			return 'ng_ok'
		else:
			return 'ng_ng'
	
	def get_level(self,score):
		if score < 0.45:
			return 1
		elif score < 0.75:
			return 2
		else:
			return 3

	def compare_label(self,label_pair,prob_pair):
		if self.add_level:
			label_score = self.get_level(label_pair['score'])
			prob_score = self.get_level(prob_pair['score'])
		else:
			label_score = 0.5
			prob_score = 0.5
		if label_pair['name'] == 'OK' and prob_pair['name'] == 'OK':
			return 'ok_true'
		elif label_pair['name'] == 'OK' and prob_pair['name'] != 'OK':
			return 'ok_over'
		elif label_pair['name'] != 'OK' and prob_pair['name'] == 'OK':
			return 'ok_miss'
		else:
			if label_score > prob_score:
				if label_pair['name'] == prob_pair['name']:
					return 'ng_miss_same'
				else:
					return 'ng_miss_diff'
			elif prob_score > label_score:
				if label_pair['name'] == prob_pair['name']:
					return 'ng_over_same'
				else:
					return 'ng_over_diff'
			else:
				if label_pair['name'] == prob_pair['name']:
					return 'same_true'
				else:
					return 'diff_true'

	def divide(self,a,b):
		if b == 0:
			return -1
		else:
			return a/b

	def calcu_global_result(self):
		raw_global_result = {'ok_true': 0., 'same_true': 0., 'diff_true': 0., 'ok_miss': 0., 'ng_miss_same': 0., 'ng_miss_diff': 0., 'ok_over': 0., 'ng_over_same': 0., 'ng_over_diff': 0.}
		raw_global_result_xml = {'ok_ok': 0., 'ok_ng': 0., 'ng_ok': 0., 'ng_ng': 0.}
		for one_pair in self.pair_list:
			raw_global_result[one_pair['res']] += 1
			if self.have_xml:
				raw_global_result_xml[one_pair['res_xml']] += 1

		total_num = 0.
		for (name,num) in raw_global_result.items():
			total_num += num
		self.global_result['总数据量'] = total_num
		self.global_result['aidi指标'] = self.divide(raw_global_result['ok_true'] + raw_global_result['same_true'] + raw_global_result['ng_miss_same'] + raw_global_result['ng_over_same'],total_num)
		self.global_result['类型精度'] = self.divide(raw_global_result['ng_miss_same'] + raw_global_result['ng_over_same'] + raw_global_result['same_true'],raw_global_result['ok_over'] + raw_global_result['ng_miss_diff'] + raw_global_result['ng_over_diff'] + raw_global_result['diff_true'] + raw_global_result['ng_miss_same'] + raw_global_result['ng_over_same'] + raw_global_result['same_true'])
		self.global_result['类型召回'] = self.divide(raw_global_result['ng_miss_same'] + raw_global_result['ng_over_same'] + raw_global_result['same_true'],total_num - raw_global_result['ok_true'] - raw_global_result['ok_over'])
		if self.add_level:
			self.global_result['程度精度'] = self.divide(raw_global_result['diff_true'] + raw_global_result['same_true'],raw_global_result['ok_over'] + raw_global_result['diff_true'] + raw_global_result['same_true'])
			self.global_result['程度召回'] = self.divide(raw_global_result['diff_true'] + raw_global_result['same_true'],total_num - raw_global_result['ok_true'] - raw_global_result['ok_over'])
			self.global_result['混淆率'] = self.divide(raw_global_result['diff_true'],raw_global_result['diff_true'] + raw_global_result['same_true'])
			self.global_result['程度类型精度'] = self.divide(raw_global_result['same_true'],raw_global_result['ok_over'] + raw_global_result['diff_true'] + raw_global_result['same_true'])
			self.global_result['程度类型召回'] = self.divide(raw_global_result['same_true'],total_num - raw_global_result['ok_true'] - raw_global_result['ok_over'])
			if self.have_xml:
				self.global_result['现场缺陷精度'] = self.divide(raw_global_result_xml['ng_ng'],raw_global_result_xml['ng_ng'] + raw_global_result_xml['ok_ng'])
				self.global_result['现场缺陷召回'] = self.divide(raw_global_result_xml['ng_ng'],raw_global_result_xml['ng_ng'] + raw_global_result_xml['ng_ok'])
				self.global_result['现场ok精度'] = self.divide(raw_global_result_xml['ok_ok'],raw_global_result_xml['ok_ok'] + raw_global_result_xml['ng_ok'])
				self.global_result['现场ok召回'] = self.divide(raw_global_result_xml['ok_ok'],raw_global_result_xml['ok_ok'] + raw_global_result_xml['ok_ng'])
				self.global_result['现场缺陷原始数'] = total_num - raw_global_result['ok_true'] - raw_global_result['ok_over']
				self.global_result['现场缺陷过滤数'] = raw_global_result_xml['ng_ng'] + raw_global_result_xml['ng_ok']
			
		for (name,value) in self.global_result.items():
			self.global_result_name.append(name)
			self.global_result_value.append(value)

		print(self.global_result)

	def copy_list(self,input_list):
		new_list = []
		for num,name in enumerate(self.name_list):
			if name == 'OK':
				new_list.append(input_list[num])
			else:
				new_list.append(input_list[num])
				new_list.append(input_list[num])
				new_list.append(input_list[num])
		return new_list

	
	def save_result(self,add_level = False):
		self.set_eval_set('train')
		self.calcu_one_result('train',add_level)
		self.set_eval_set('test')
		self.calcu_one_result('test',add_level)
		self.tool.save()
	
	def calcu_one_result(self,sheet_name,add_level = False):
		if add_level:
			self.set_add_level(True)	
			self.matrix = self.get_matrix()
			self.reduce_matrix_row = self.get_matrix_reduce()
			self.reduce_matrix_col = self.get_matrix_reduce(False)
			matrix_len = len(self.matrix)
			
			self.tool.draw_matrix(sheet_name,0,0,self.matrix,self.name_level_list)
			self.tool.draw_col(sheet_name,0,matrix_len + 1,['细分精度'])
			self.tool.draw_col(sheet_name,1,matrix_len + 1,self.get_result('pr'))

			self.tool.draw_col(sheet_name,0,matrix_len + 2,['细分召回'])
			self.tool.draw_col(sheet_name,1,matrix_len + 2,self.get_result('rc'))

			self.tool.draw_col(sheet_name,0,matrix_len + 3,['细分总数'])
			self.tool.draw_col(sheet_name,1,matrix_len + 3,self.get_total_num())

			self.set_add_level(False)	
			self.matrix = self.get_matrix()
			self.reduce_matrix_row = self.get_matrix_reduce()
			self.reduce_matrix_col = self.get_matrix_reduce(False)

			self.tool.draw_col(sheet_name,0,matrix_len + 4,['单类精度'])
			self.tool.draw_col(sheet_name,1,matrix_len + 4,self.copy_list(self.get_result('pr')))

			self.tool.draw_col(sheet_name,0,matrix_len + 5,['单类召回'])
			self.tool.draw_col(sheet_name,1,matrix_len + 5,self.copy_list(self.get_result('rc')))

			total_num = self.get_total_num()
			self.tool.draw_col(sheet_name,0,matrix_len + 6,['单类总数'])
			self.tool.draw_col(sheet_name,1,matrix_len + 6,self.copy_list(total_num))

			self.set_add_level(True)
			self.compare()
			index_num = 7
			if self.have_xml:
				index_num += 2
				miss_num = self.get_miss_num()
				miss_rate = []
				for index,num in enumerate(total_num):
					miss_rate.append(self.divide(miss_num[index],total_num[index]))		
				self.tool.draw_col(sheet_name,0,matrix_len + 7,['漏检数'])
				self.tool.draw_col(sheet_name,1,matrix_len + 7,self.copy_list(miss_num))

				self.tool.draw_col(sheet_name,0,matrix_len + 8,['漏检率'])
				self.tool.draw_col(sheet_name,1,matrix_len + 8,self.copy_list(miss_rate))

			self.tool.draw_col(sheet_name,0,matrix_len + index_num,['排序号'])
			self.tool.draw_col(sheet_name,1,matrix_len + index_num,[i for i in range(matrix_len)])

		else:
			self.set_add_level(False)	
			self.matrix = self.get_matrix()
			self.reduce_matrix_row = self.get_matrix_reduce()
			self.reduce_matrix_col = self.get_matrix_reduce(False)
			matrix_len = len(self.matrix)
			
			self.tool.draw_matrix(sheet_name,0,0,self.matrix,self.name_list)
			self.tool.draw_col(sheet_name,0,matrix_len + 1,['精度'])
			self.tool.draw_col(sheet_name,1,matrix_len + 1,self.get_result('pr'))

			self.tool.draw_col(sheet_name,0,matrix_len + 2,['召回'])
			self.tool.draw_col(sheet_name,1,matrix_len + 2,self.get_result('rc'))

			self.tool.draw_col(sheet_name,0,matrix_len + 3,['总数'])
			self.tool.draw_col(sheet_name,1,matrix_len + 3,self.get_total_num())

			self.tool.draw_col(sheet_name,0,matrix_len + 4,['排序号'])
			self.tool.draw_col(sheet_name,1,matrix_len + 4,[i for i in range(matrix_len)])
			self.compare()


		self.calcu_global_result()
		if sheet_name == 'train':
			self.tool.draw_row('global_eval',0,0,['训练集'])
			self.tool.draw_row('global_eval',1,0,self.global_result_name)
			self.tool.draw_row('global_eval',2,0,self.global_result_value)
		else:
			self.tool.draw_row('global_eval',5,0,['测试集'])
			self.tool.draw_row('global_eval',6,0,self.global_result_name)
			self.tool.draw_row('global_eval',7,0,self.global_result_value)


	def get_matrix(self):
		if self.add_level:
			matrix = self.init_matrix(self.name_level_list)
		else:
			matrix = self.init_matrix(self.name_list)
		label_prob_matrix = copy.deepcopy(matrix)
		for one_pair in self.pair_list:
			if self.add_level:
				label_prob_matrix[self.get_name_level(one_pair['label'])][self.get_name_level(one_pair['prob'])] += 1
			else:
				label_prob_matrix[one_pair['label']['name']][one_pair['prob']['name']] += 1		
		return label_prob_matrix
	
	def get_matrix_reduce(self, base_row = True):
		matrix_reduce = {}
		if base_row:
			for (name_row, dict_tmp) in self.matrix.items():
				total = 0
				for (name_col, num) in dict_tmp.items():
					total += num
				matrix_reduce[name_row] = total
		else:
			flag = True
			for (name_row, dict_tmp) in self.matrix.items():
				if flag:
					matrix_reduce =  copy.deepcopy(dict_tmp)
					flag = False
					continue
				else:
					for (name_col, num) in dict_tmp.items():
						matrix_reduce[name_col] += num
		return matrix_reduce

	def get_name_level(self, one_data):
		if one_data['name'] == 'OK':
			return 'OK'
		if one_data['score'] < 0.45:
			return one_data['name'] + '_轻度'
		if one_data['score'] < 0.75:
			return one_data['name'] + '_中度'
		return one_data['name'] + '_严重'


	def get_name_score(self,one_label_path):
		if one_label_path.endswith('json'):
			with open(one_label_path, 'r', encoding='utf8') as fp:
				json_data = json.load(fp)
				return json_data[0]['label'], json_data[0]['score']
		else:
			in_label = LabelIO()
			in_label.read_from(one_label_path)
			json_label = json.loads(in_label.to_json())
			return json_label['regions'][0]['name'], json_label['regions'][0]['score']

	def make_pair(self,label_name,label_score):
		one_data = {}
		one_data['name'] = label_name
		one_data['score'] = label_score
		return one_data
	
	def trans_name(self,label_name,score):
		split_name = label_name.split('_')
		if len(split_name) > 1:
			if split_name[1] == '轻度':
				return self.make_pair(split_name[0],0.3)
			elif split_name[1] == '中度':
				return self.make_pair(split_name[0],0.6)
			else:
				return self.make_pair(split_name[0],0.9)
		else:
			return self.make_pair(label_name, score)
	
	def set_list_src(self,list_src):
		self.list_src = list_src

	def get_name_score_list(self):
		if self.list_src == 'db':
			self.get_list()
		else:
			self.get_task_list()
		pair_list = []
		name_list = []
		label_suffix = self.get_label_suffix()
		for one_index in self.set_list:
			one_pair = {}
			label_path = self.root_dir + '/label/' + str(one_index) + label_suffix
			prob_path = self.root_dir + '/test_result/' + str(one_index) + label_suffix
			if not os.path.exists(prob_path):
				continue
			try:
				label_name, label_score = self.get_name_score(label_path)
				prob_name, prob_score = self.get_name_score(prob_path)
			except:
				print(label_path)
				continue

			split_label_name = label_name.split('_')
			split_prob_name = prob_name.split('_')
			if split_label_name[0] not in name_list:
				name_list.append(split_label_name[0])
			if split_prob_name[0] not in name_list:
				name_list.append(split_prob_name[0])

			one_pair['label'] = self.trans_name(label_name,label_score)
			one_pair['prob'] = self.trans_name(prob_name,prob_score)
			pair_list.append(one_pair)
		return name_list,pair_list

		
if __name__ == '__main__':
	# out_path = 'D:/yang.xie/data/数据分析/channel3.xlsx'
	# root_dir = 'D:/yang.xie/aidi_projects/20201117-iteration4/channel3/RegClassify_0'

	# out_path = 'D:/yang.xie/data/数据分析/cls_roi_R101_1500iter.xlsx'
	# root_dir = r'D:\yang.xie\aidi_projects\20201203-ROI-bias\cls_roi\Classify_0'	

	out_path = 'D:/yang.xie/data/数据分析/20210127-kt/cls_64_v1.xlsx'
	
	root_dir = r'D:\yang.xie\aidi_projects\20210105-multi-cls\cls_aqimg\Classify_0'
	print(out_path)
	eval_set = eval_tools(root_dir,out_path)
	# eval_set.set_list_src('task')
	eval_set.save_result(False)
		