import os
import sys
import json
import random
import sqlite3
import numpy as np
import plotly.figure_factory as ff
sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *

class analyse():
	def __init__(self,root_dir):
		self.root_dir = root_dir
		self.eval_set = 'test'
		self.train_list = []
		self.test_list = []

	def get_db_file(self):
		for one_file in os.listdir(self.root_dir + '/..'):
			if one_file.endswith('.db'):
				return self.root_dir + '/../' + one_file
		print('Can not find db file!')
		return ''

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
			set_list = [row[0] for row in cursor]

		return set_list

	def get_label_suffix(self):
		for one_label in os.listdir(self.root_dir + '/label'):
			if one_label.endswith('.aqlabel'):
				return '.aqlabel'
			elif one_label.endswith('.json'):
				return '.json'
		print('Label suffix error!')
		return ''

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

	def get_data_list(self):
		data_list = []
		label_suffix = self.get_label_suffix()
		set_list = self.get_list()
		
		for one_index in set_list:
			one_pair = {}
			label_path = self.root_dir + '/label/' + str(one_index) + label_suffix
			prob_path = self.root_dir + '/test_result/' + str(one_index) + label_suffix

			label_name, label_score = self.get_name_score(label_path)
			prob_name, prob_score = self.get_name_score(prob_path)
			data_list.append({'set':self.eval_set,'label_path':label_path,'prob_path':prob_path,'label_name':label_name,'label_score':label_score,'prob_name':prob_name,'prob_score':prob_score})		
		return data_list

	def set_eval_set(self,eval_set):
		self.eval_set = eval_set
	
	def get_process_data(self):
		self.set_eval_set('test')
		data_list = self.get_data_list()
		true_list = []
		false_list = []

		tmp_list = []

		for one_data in data_list:
			# if one_data['label_name'] == 'OK' and one_data['prob_name'] == '多铣':
			# 	print(one_data['prob_path'])

			# if one_data['prob_name'] == 'OK':
			if one_data['label_name'] == '小焊盘沾油墨':
				if one_data['label_name'] == one_data['prob_name']:
					true_list.append(one_data['prob_score'])
					if one_data['prob_score'] > 0.9:
						tmp_list.append(one_data['prob_score'])

				else:
					false_list.append(one_data['prob_score'])
					if one_data['prob_score'] > 0.9:
						print(one_data['prob_path'])
		print('tmp_list:', len(tmp_list))
		return true_list,false_list



if __name__ == '__main__':
	root_dir = 'D:/yang.xie/aidi_projects/20201117-iteration4/classify_30_ok/Classify_0'
	tool = analyse(root_dir)
	true_list,false_list = tool.get_process_data()

	print(len(true_list))
	print(len(false_list))

	hist_data = [np.array(true_list),np.array(false_list)]
	group_labels = ['小焊盘沾油墨-true', '小焊盘沾油墨-false']

	fig = ff.create_distplot(hist_data, group_labels, bin_size=.2)
	fig.show()













# import os
# import sys
# import json
# sys.path.insert(0,'D:/yang.xie/packages')
# from aidi410_label.aidi_vision import *


# def get_name_score(one_label_path):
# 	in_label = LabelIO()
# 	in_label.read_from(one_label_path)
# 	json_label = json.loads(in_label.to_json())
# 	name_score_list = []
# 	name_score_list.append({'select_name':json_label['regions'][0]['name'],'score':json_label['regions'][0]['score']})
# 	for one_point in json_label['regions'][0]['key_points']:
# 		one_dict = {}
# 		one_dict['name'] = one_point['name']
# 		one_dict['score'] = one_point['score']
# 		name_score_list.append(one_dict)
# 	return name_score_list


# if __name__=="__main__":
# 	if (len(sys.argv)) != 2:
# 		print('Needs a file path.')
# 		sys.exit()
# 	name_score_list = get_name_score(sys.argv[1])
# 	sum_score = 0
# 	sum_score_abs = 0
# 	count = 0
# 	for one_name_score in name_score_list:
# 		try:
# 			if count < 4:
# 				print(one_name_score['name'],': ',one_name_score['score'])
# 			sum_score += one_name_score['score']
# 			if one_name_score['score'] > 0:
# 				sum_score_abs += one_name_score['score']
# 			count += 1
# 		except:
# 			print(one_name_score['select_name'],': ',one_name_score['score'])
# 	# print('total score minus: ',sum_score)
# 	print('total score: ',sum_score_abs)

