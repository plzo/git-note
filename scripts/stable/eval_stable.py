
import os
import sys
import shutil
import json
import cv2
import numpy as np
import math
import random

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

def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

# print(res['regions'][0]['polygon']['inners'][0]['points'])
# img_path = r'F:\yang.xie\data\20221205_stable\AIDI_projects\base\Segment_0\mask.png'
# image = cv2.imread(img_path)
# image =cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# contours2, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def find_contours_aqlabel(aqlabel_path):
	res = read_label(aqlabel_path)
	# print(res)

	ret = []
	for region in res['regions']:
		tmp_dict = {}
		contours = []
		point_list = []
		for p in region['polygon']['outer']['points']:
			point = []
			point.append(int(p['x']))
			point.append(int(p['y']))
			point_list.append([point])
		contours.append(np.array(point_list))

		for one_inner in region['polygon']['inners']:
			point_list = []
			for p in one_inner['points']:
				point = []
				point.append(int(p['x']))
				point.append(int(p['y']))
				point_list.append([point])
			contours.append(np.array(point_list))
		tmp_dict['name'] = region['name']
		tmp_dict['contours'] = contours
		ret.append(tmp_dict)
	
	return ret, (res['img_size']['height'],res['img_size']['width'])

def find_center(contour):
	M = cv2.moments(contour)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	return (cX,cY)

def center_distance(c1,c2):
	return math.sqrt(math.pow(c1[0]-c2[0],2) + math.pow(c1[1]-c2[1],2))

def calcu_distance(label_contours, result_contours):
	label_center = find_center(label_contours[0])
	min_distance = 9999999
	for c in result_contours:
		result_center = find_center(c)
		one_distance = center_distance(label_center,result_center)
		if one_distance < min_distance:
			min_distance = one_distance
	return min_distance

miss_list = []

def math_contours(label,result,threshold):
	label_name_contours, label_size = find_contours_aqlabel(label)
	result_name_contours, result_size = find_contours_aqlabel(result)
	final_name_contours = []
	for label_name_contour in label_name_contours:
		tmp_dict = {}
		tmp_dict['name'] = label_name_contour['name']
		tmp_dict['contours'] = []
		min_region_distance = 9999999
		label_contours = label_name_contour['contours']
		for result_name_contour in result_name_contours:
			result_contours = result_name_contour['contours']
			one_distance = calcu_distance(label_contours,result_contours)
			if one_distance < min_region_distance:
				min_region_distance = one_distance
				tmp_dict['contours'] = result_contours
		if min_region_distance > threshold:
			miss_list.append(result)
			tmp_dict['contours'] = []
		final_name_contours.append(tmp_dict)
	return final_name_contours, label_size

def calcu_area(contours):
	if len(contours)==0:
		return 0
	area = cv2.contourArea(contours[0])
	if len(contours) == 1:
		return area
	for i in range(1,len(contours)):
		area = area - cv2.contourArea(contours[i])
	return area

def calcu_w(contours):
	if len(contours)==0:
		return 0
	x,y,w,h = cv2.boundingRect(contours[0])
	return w

def calcu_h(contours):
	if len(contours)==0:
		return 0
	x,y,w,h = cv2.boundingRect(contours[0])
	return h

def get_average(datas):
	return sum(datas)/len(datas)

def get_variance(datas):
	ave = get_average(datas)
	# return math.sqrt(sum([(x - ave) ** 2 for x in datas]) / len(datas)) / ave
	return sum([(x - ave) ** 2 for x in datas]) / len(datas)

def contours_variance(contours_list, fc, flag=False):

	value_list = []
	for contours in contours_list:
		value = fc(contours)
		value_list.append(value)
	if flag:
		print(value_list)

	return get_variance(value_list)

def global_iou(contours_list):
	w_max = 0
	h_max = 0
	for contours in contours_list:
		if len(contours)==0:
			return 0,1
		x,y,w,h = cv2.boundingRect(contours[0])
		if w > w_max:
			w_max = w
		if h > h_max:
			h_max = h
			
	new_contours_list = []
	for contours in contours_list:
		(x,y) = find_center(contours[0])
		w_offset = w_max - x
		h_offset = h_max - y
		new_contours = []
		for contour in contours:
			point_list = []
			for p in contour:
				point = []
				point.append(p[0][0] + w_offset)
				point.append(p[0][1] + h_offset)
				point_list.append([point])
			new_contours.append(np.array(point_list))
		new_contours_list.append(new_contours)
	
	# print(new_contours_list[0])
	
	img_list = []
	for new_contours in new_contours_list:
		img = 255 * np.ones((2 * h_max,2 * w_max), dtype=np.uint8)
		img = cv2.drawContours(img, new_contours, -1, (0), -1)
		img_list.append(img)
		# cv2.imshow('img',img)
		# cv2.waitKey(0)
	count_and = 0
	count_or = 0
	for r in range(2 * h_max):
		for c in range(2 * w_max):
			for img in img_list:
				if img[r][c] == 0:
					count_or += 1
					break
			all_0 = True
			for img in img_list:
				if img[r][c] == 255:
					all_0 = False
					break
			if all_0:
				count_and += 1

	# print('count_and: ', count_and)
	# print('count_or: ', count_or)
	return count_and,count_or

def add_name(name_contours):
	if len(name_contours) == 0:
		return name_contours
	if len(name_contours) == 1:
		name_contours[0]['name'] = 'n1'
		return name_contours

	tmp_dict = {}
	tmp_list = []
	new_name_contours = []
	for i in range(len(name_contours)):
		if len(name_contours[i]['contours']) == 0:
			continue
		(cx,xy) = find_center(name_contours[i]['contours'][0])
		tmp_dict[cx] = name_contours[i]['contours']
		tmp_list.append(cx)

	tmp_list.sort()
	for i in range(len(tmp_list)):
		tmp_dict2 = {}
		tmp_dict2['name'] = 'n' + str(i+1)
		tmp_dict2['contours'] = tmp_dict[tmp_list[i]]
		new_name_contours.append(tmp_dict2)
	return new_name_contours


def eval(root_dir):
	no_label = True
	# no_label = False
	threshold = 200
	if no_label:
		threshold = 2000

	# img_num = 6
	# start_index = 7
	# end_index = 66

	img_num = 10
	start_index = 11
	end_index = 650

	defects_contours_list = []
	for i in range(img_num):
		# eval_index = [j for j in range(start_index + i, end_index, img_num)]
		eval_index = [j for j in range(start_index + i * 64, start_index + i * 64 + 64)]

		tmp_list = []
		name_contours_set = {}
		for index in eval_index:
			label_path = root_dir + '/label/' + str(index) + '.aqlabel'
			if no_label:
				label_path = root_dir + '/test_result/' + str(eval_index[0]) + '.aqlabel'
			result_path = root_dir + '/test_result/' + str(index) + '.aqlabel'
			name_contours, size = math_contours(label_path, result_path, threshold)

			name_count = 0
			if no_label:
				name_contours = add_name(name_contours)
				# for i in range(len(name_contours)):
				# 	name_contours[i]['name'] = 'n' + str(name_count)
				# 	name_count += 1
			tmp_list.append(name_contours)
			

		for name_contour in tmp_list[0]:
			name_contours_set[name_contour['name']] = []

		for name_contours in tmp_list:
			for name_contour in name_contours:
				name_contours_set[name_contour['name']].append(name_contour['contours'])

		for name in name_contours_set:
			defects_contours_list.append(name_contours_set[name])


	area_variance_list = []
	w_variance_list = []
	h_variance_list = []
	global_iou_list = []
	count_and_list = []
	count_or_list = []

	for contours_list in defects_contours_list:
		area_variance_list.append(contours_variance(contours_list, calcu_area))
		w_variance_list.append(contours_variance(contours_list, calcu_w))
		h_variance_list.append(contours_variance(contours_list, calcu_h))
		count_and, count_or = global_iou(contours_list)
		global_iou_list.append((count_and,count_or))
		count_and_list.append(count_and)
		count_or_list.append(count_or)
	
	print(area_variance_list)
	print(w_variance_list)
	print(h_variance_list)
	print(sum(area_variance_list)/len(area_variance_list))
	print(sum(w_variance_list)/len(w_variance_list))
	print(sum(h_variance_list)/len(h_variance_list))

	print('global_iou_list:', global_iou_list)
	print('global_iou: ', sum(count_and_list)/sum(count_or_list))
	print('miss_list: ')
	for m in miss_list:
		print(m)



	# area_variance_list = []
	# for name in name_contours_set:
	# 	contours_set = name_contours_set[name]
	# 	area_list = []
	# 	for contours in contours_set:
	# 		area = calcu_area(contours)
	# 		area_list.append(area)
	# 	print(area_list)
	# 	area_variance_list.append(get_variance(area_list))
	# print(area_variance_list)

	# one_contours = name_contours_set['n1'][0]
	# img = 255 * np.ones(size, dtype=np.uint8)
	# img = cv2.drawContours(img, one_contours, -1, (0), -1)
	# cv2.imshow('img',img)
	# cv2.waitKey(0)
	


if __name__ == '__main__':
	# root_dir = r'F:\yang.xie\data\20221205_stable\AIDI_projects\base\Segment_0'
	# eval(root_dir)

	root_dir = r'F:\yang.xie\data\20221205_stable\AIDI_projects\03-101-V2\Segment_0'
	eval(root_dir)


	# random_list = []
	# for i in range(10000):
	# 	random_list.append(random.random())
	# print(get_variance(random_list))
