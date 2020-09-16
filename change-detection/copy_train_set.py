import os
import sys
import shutil
import json
import random

origin_dir = './label0725_test_classify7/RegClassify_0'
select_dir = './label0725_test_classify_nolabel/RegClassify_0'
target_dir = './select0812'

# class_name = '金面_清晰'
# class_name = '金面_较清晰'
# class_name = '金面_杂乱模糊'

# class_name = '区域色差_条纹'
# class_name = '区域色差_亮度'
# class_name = '区域色差_部分'
# class_name = '正常元素_延伸光滑'
# class_name = '正常元素_金面延伸_微'
# class_name = '正常元素_错位'
# class_name = '正常元素_多防焊'
# class_name = '防焊_模糊'
# class_name = '防焊_线条'
# class_name = '防焊_清晰'
# class_name = '跨区域_清晰'
# class_name = '跨区域_模糊'
# class_name = '跨区域_污染模糊'
# class_name = '毛刺_板边'
# class_name = '毛刺_孔'

# class_name = '黑色竖划伤'
# class_name = '字符型'
# class_name = '混合缺陷'
# class_name = '小目标_清晰点'
# class_name = '错位_堵孔'
# class_name = '错位_孔偏'
class_name = '错误'




target_class_source_dir = target_dir + '/'+ class_name + '/source'
target_class_label_dir = target_dir + '/'+ class_name + '/label'
if not os.path.exists(target_class_source_dir):
	os.makedirs(target_class_source_dir)
if not os.path.exists(target_class_label_dir):
	os.makedirs(target_class_label_dir)

target_all_source_dir = target_dir + '/all/source'
target_all_label_dir = target_dir + '/all/label'
if not os.path.exists(target_all_source_dir):
	os.makedirs(target_all_source_dir)
if not os.path.exists(target_all_label_dir):
	os.makedirs(target_all_label_dir)

origin_source_dir = origin_dir + '/source'
origin_label_dir = origin_dir + '/label'
select_source_dir = select_dir + '/source'
select_label_dir = select_dir + '/label'

def copy_files():
	max_count = len(os.listdir(origin_source_dir)) - len(os.listdir(select_source_dir)) - len(os.listdir(target_all_source_dir))
	count = 0
	print(max_count)
	for one_source in os.listdir(origin_source_dir):
		one_label = one_source.strip().split('.')[0] + '.aqlabel'
		# print(one_label)
		if one_source not in os.listdir(select_source_dir) and one_source not in os.listdir(target_all_source_dir):
			shutil.copy(origin_source_dir + '/' + one_source, target_all_source_dir + '/' + one_source)	
			shutil.copy(origin_source_dir + '/' + one_source, target_class_source_dir + '/' + one_source)
			shutil.copy(origin_label_dir + '/' + one_label, target_class_label_dir + '/' + one_label)
			shutil.copy(origin_label_dir + '/' + one_label, target_all_label_dir + '/' + one_label)
			count += 1
		if count == max_count:
			break

def copy_files_with_json(json_dir, source_source_dir, source_label_dir, target_root_dir):
	for one_json in os.listdir(json_dir):
		json_str = open(os.path.join(json_dir,one_json),'r', encoding='UTF-8')
		json_dict = json.load(json_str)
		class_name = json_dict[0]['label']
		class_dir = os.path.join(target_root_dir, class_name)

		target_source_dir = os.path.join(class_dir, 'source')
		target_label_dir = os.path.join(class_dir, 'label')
		if not os.path.exists(target_source_dir):
			os.makedirs(target_source_dir)
		if not os.path.exists(target_label_dir):
			os.makedirs(target_label_dir)
		one_label = one_json.strip().split('.')[0] + '.aqlabel'
		one_source = one_json.strip().split('.')[0] + '.aqimg'

		source_source_path = os.path.join(source_source_dir, one_source)
		target_source_path = os.path.join(target_source_dir, one_source)

		source_label_path = os.path.join(source_label_dir, one_label)
		target_label_path = os.path.join(target_label_dir, one_label)

		if os.path.exists(source_source_path):
			shutil.copy(source_source_path, target_source_path)	
			shutil.copy(source_label_path, target_label_path)
		else:
			print('file not exist:',source_source_path)


def analysis_display(root_dir):
	for sub_dir in os.listdir(root_dir):
		print(sub_dir,'\t',len(os.listdir(os.path.join(root_dir,sub_dir)+'/source')))


def label_intersection(dir1, dir2, output_dir):
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	for one_file in os.listdir(dir1):
		if one_file in os.listdir(dir2):
			shutil.copy(dir1 + '/' + one_file, output_dir + '/' + one_file)

if __name__ == '__main__':
	# copy_files()
	# json_dir = './Reg_Project0529_1/RegClassify_0/label'
	# source_source_dir = './label0725_test_classify7/RegClassify_0/source'
	# source_label_dir = './label0725_test_classify7/RegClassify_0/label'
	# target_root_dir = './classify_with_json0813'
	# # copy_files_with_json(json_dir,source_source_dir,source_label_dir,target_root_dir)
	# analysis_display(target_root_dir)
	# analysis_display('./select0812')
	label_intersection('F:/yang.xie/aidi/class0808/class0808_label/class0808_class_train/Segment_0/label','F:/yang.xie/aidi/label0725/train0814/all/label','./label_tmp')


					



