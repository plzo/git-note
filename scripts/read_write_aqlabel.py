
import os
import sys
import shutil
import json
sys.path.insert(0,'D:/yang.xie/packages')
from aidi_vision430.aidi_vision import *

def read_label(label_path):
	in_label = LabelIO()
	in_label.read_from(label_path)
	json_label = json.loads(in_label.to_json())
	return json_label

def write_label(label_path, json_label):
	json_str = json.dumps(json_label,ensure_ascii=False)
	out_label = LabelIO()
	out_label.from_json(json_str)
	out_label.save_to(label_path)

def find_empty_label(label_dir):
	sum_num = len(os.listdir(label_dir))
	count = 0
	error_list = []
	for one_label in os.listdir(label_dir):
		one_label_path = label_dir + '/' + one_label
		json_label = read_label(one_label_path)
		count += 1
		if len(json_label['regions']) < 1:
			error_list.append(one_label_path)
			if count % 100 == 0:
				print('remain: ', sum_num - count)
	print('错误的label: ')
	for one_error_path in error_list:
		print(one_error_path)
			


if __name__ == '__main__':
	label_dir = r'F:\yang.xie\data\20220620_PCB\data5000_train\Classify_0\label'
	find_empty_label(label_dir)

	# label_path = r'F:\yang.xie\data\20220620_PCB\data5000_train\Classify_0\label\2.aqlabel'
	# out_path = r'F:\yang.xie\projects\20220525_pcb\aidi_pcb_2c_small\Classify_0\label\tmp.aqlabel'
	# json_label = read_label(label_path)
	# print(len(json_label['regions']))
	# print(json_label)
	# print(len(json_label['regions']))
	# write_label(out_path, json_label)