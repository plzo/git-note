
import os
import sys
import shutil
import json
sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *


def get_name_score(one_label_path):
	if one_label_path.endswith('json'):
		with open(one_label_path, 'r', encoding='utf8') as fp:
			json_data = json.load(fp)
			return json_data[0]['label'], json_data[0]['score']
	else:
		in_label = LabelIO()
		in_label.read_from(one_label_path)
		json_label = json.loads(in_label.to_json())
		return json_label['regions'][0]['name'], json_label['regions'][0]['score']

def change_label(one_label_path):
	# name,score = get_name_score(one_label_path)
	# print(name,score)
	in_label = LabelIO()
	in_label.read_from(one_label_path)
	json_label = json.loads(in_label.to_json())
	# json_label['regions'][0]['score'] = 0.5
	json_str = json.dumps(json_label,ensure_ascii=False).encode("utf-8").decode("GBK")

	out_label = LabelIO()
	print(json_str)
	out_label.from_json(json_str)
	out_label.save_to(one_label_path)

def trans_name(name,score):
	if name == 'OK':
		return name
	if len(name.split('_')) > 1:
		return name
	if score < 0.45:
		return name + '_轻度'
	elif score < 0.75:
		return name + '_中度'
	else:
		return name + '_严重'



def change_label2(project_dir,one_label,save_path):
	# json_path = 'D:/yang.xie/aidi_projects/project-20201022/classify_no_reg/Classify_0/label/1.json'
	# img_path = 'D:/yang.xie/aidi_projects/project-20201022/classify_no_reg/Classify_0/source/1.aqimg'

	json_path = project_dir + '/tmp.json'
	img_path = project_dir + '/source/' + one_label.split('.')[0] + '.aqimg'
	src_label_path = project_dir + '/label/' + one_label

	print(json_path)

	name,score = get_name_score(src_label_path)
	name = trans_name(name,score)
	json_dict = [{'label':name,'score':score}]
	json.dump(json_dict, open(json_path, 'w',encoding='UTF-8'),ensure_ascii=False)

	out_label = LabelIO()
	read_33X_classify_label(json_path, img_path, out_label)
	out_label.save_to(save_path)

def change_dir(project_dir):
	if not os.path.exists(project_dir + '/label_changed'):
		os.makedirs(project_dir + '/label_changed')
	for one_label in os.listdir(project_dir + '/label'):
		one_label_path = project_dir + '/label/' + one_label
		save_path = project_dir + '/label_changed/' + one_label
		change_label2(project_dir,one_label,save_path)





if __name__ == '__main__':
	label_path = 'D:/yang.xie/aidi_projects/20201117-iteration4/classify_no_reg_3level/Classify_0'
	change_dir(label_path)

