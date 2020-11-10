import os
import sys
import shutil
import json
sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *

def change_test(one_label_path):
	# in_label = LabelIO()
	# in_label.read_from(one_label_path)
	# json_label = json.loads(in_label.to_json())

	# # json_label['name'] = 'change'

	# data = in_label.mutable_data()

	# out_label = LabelIO()
	# str_label = json.dumps(json_label)
	# res = out_label.from_json(str_label)
	# json_label2 = json.loads(out_label.to_json())
	# out_label.save_to(one_label_path)


	# in_label = LabelIO()
	# in_label.read_from(one_label_path)
	# tmp = in_label.to_json()
	# json_label = json.loads(tmp)
	# print(in_label.data2str())

	# out_label = LabelIO()
	# print(tmp)
	# print(out_label.from_json(tmp))

	# json_label2 = json.loads(out_label.to_json())
	# print(json_label2)

	# out_label = LabelIO()
	json_dict = {"dataset_type":"Classify","img_size":{"width":128,"height":128},"name":"","score":0,"regions":[{"polygon":{"outer":{"points":[{"x":0,"y":0},{"x":0,"y":128},{"x":128,"y":128},{"x":128,"y":0}]},"inners":[]},"name":"test_name","score":0.9,"key_points":[],"ext_info":{}}],"masks":[],"hardcases":[],"ext_info":{}}
	# json_str = json.dumps(json_dict)
	json.dump(json_dict, open('D:/yang.xie/aidi_projects/project-20201022/classify_no_reg/Classify_0/label/1.json', 'w',encoding='UTF-8'),ensure_ascii=False)
	json_path = 'D:/yang.xie/aidi_projects/project-20201022/classify_no_reg/Classify_0/label/1.json'
	img_path = 'D:/yang.xie/aidi_projects/project-20201022/classify_no_reg/Classify_0/source/1.aqimg'
	i_label = LabelIO()
	# read_33X_classify_label(json_path, img_path, i_label)
	i_label.read_from(json_path)
	i_label.save_to(one_label_path)

	# print(json_str)
	# res = out_label.from_json(json_str)
	# print(res)
	# json_label = json.loads(out_label.to_json())
	# print(json_label)











if __name__ == '__main__':
	label_path = 'D:/yang.xie/aidi_projects/project-20201022/classify_no_reg/Classify_0/label/1.aqlabel'
	change_test(label_path)