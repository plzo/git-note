import os
import sys
import json
sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *


def get_name_score(one_label_path):
	in_label = LabelIO()
	in_label.read_from(one_label_path)
	json_label = json.loads(in_label.to_json())
	name_score_list = []
	name_score_list.append({'select_name':json_label['regions'][0]['name'],'score':json_label['regions'][0]['score']})
	for one_point in json_label['regions'][0]['key_points']:
		one_dict = {}
		one_dict['name'] = one_point['name']
		one_dict['score'] = one_point['score']
		name_score_list.append(one_dict)
	return name_score_list


if __name__=="__main__":
	if (len(sys.argv)) != 2:
		print('Needs a file path.')
		sys.exit()
	name_score_list = get_name_score(sys.argv[1])
	sum_score = 0
	sum_score_abs = 0
	count = 0
	for one_name_score in name_score_list:
		try:
			if count < 4:
				print(one_name_score['name'],': ',one_name_score['score'])
			sum_score += one_name_score['score']
			if one_name_score['score'] > 0:
				sum_score_abs += one_name_score['score']
			count += 1
		except:
			print(one_name_score['select_name'],': ',one_name_score['score'])
	# print('total score minus: ',sum_score)
	print('total score: ',sum_score_abs)

