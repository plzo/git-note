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

def display_json(json_dir):
	class_list = []
	class_dict = {}
	for one_json in os.listdir(json_dir):
		json_str = open(os.path.join(json_dir,one_json),'r', encoding='UTF-8')
		json_dict = json.load(json_str)
		class_name = json_dict[0]['label']
		if class_name not in class_list:
			class_list.append(class_name)
			class_dict[class_name] = 1
		else:
			class_dict[class_name] += 1
	for one_name in class_list:
		print(one_name)
	print(class_list)
	print(len(class_list))



def analysis_display(root_dir):
	count = 0
	for sub_dir in os.listdir(root_dir):
		print(sub_dir,'\t',len(os.listdir(os.path.join(root_dir,sub_dir)+'/source')))
		count = count + len(os.listdir(os.path.join(root_dir,sub_dir)+'/source'))
	print('all nums: ', count)


def label_intersection(dir1, dir2, output_dir):
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	for one_file in os.listdir(dir1):
		if one_file in os.listdir(dir2):
			shutil.copy(dir1 + '/' + one_file, output_dir + '/' + one_file)

def find_label(source_dir, label_src, label_dst):
	if not os.path.exists(label_dst):
		os.makedirs(label_dst)
	for one_source in os.listdir(source_dir):
		one_label = one_source.split('.')[0] + '.aqlabel'
		shutil.copy(label_src + '/' + one_label, label_dst + '/' + one_label)

def select_test_set(all_dir, train_dir, test_dir):
	if not os.path.exists(test_dir):
		os.makedirs(test_dir)
	ignore_list = ['all', '错误', '混合缺陷']
	for one_class in os.listdir(all_dir):
		if one_class not in ignore_list:
			test_class_source_dir = test_dir + '/' + one_class + '/source'
			test_class_label_dir = test_dir + '/' + one_class + '/label'
			if not os.path.exists(test_class_source_dir):
				os.makedirs(test_class_source_dir)
			if not os.path.exists(test_class_label_dir):
				os.makedirs(test_class_label_dir)

			train_source_dir = train_dir + '/' + one_class + '/source'
			all_source_dir = all_dir + '/' + one_class + '/source'
			select_count = int(len(os.listdir(train_source_dir)) / 0.7 * 0.3)

			selected_list = []
			for one_file in os.listdir(all_source_dir):
				if one_file not in os.listdir(train_source_dir):
					selected_list.append(one_file)
			
			res_list = []
			max_count = len(selected_list)
			count = 0
			for i in range(max_count):
				num = int(random.random() * len(selected_list))
				res_list.append(selected_list[num])
				selected_list.pop(num)
				count = count + 1
				if len(selected_list) == 0 or count >= select_count:
					break
			
			for one_source in res_list:
				src_source_file = all_source_dir + '/' + one_source
				dst_source_file = test_class_source_dir + '/' + one_source

				one_label = one_source.strip().split('.')[0] + '.aqlabel'

				src_label_file = all_dir + '/' + one_class + '/label/' + one_label
				dst_label_file = test_class_label_dir + '/' + one_label

				shutil.copy(src_source_file, dst_source_file)
				shutil.copy(src_label_file, dst_label_file)


def move_to_all(root_dir):
	ignore_list = ['OK', '区域色差_部分', '小目标_清晰点', '正常元素_延伸光滑', '毛刺_孔', '金面_较清晰', '防焊_模糊', 'all', 'all_src']
	root_all_source_dir = root_dir + '/all/source'
	root_all_label_dir = root_dir + '/all/label'
	if not os.path.exists(root_all_source_dir):
		os.makedirs(root_all_source_dir)
	if not os.path.exists(root_all_label_dir):
		os.makedirs(root_all_label_dir)
	for one_dir in os.listdir(root_dir):
		if one_dir not in ignore_list:
			for one_source in os.listdir(root_dir + '/' + one_dir + '/source'):
				shutil.copy(root_dir + '/' + one_dir + '/source/' + one_source, root_dir + '/all/source/' + one_source)
			for one_label in os.listdir(root_dir + '/' + one_dir + '/label'):
				shutil.copy(root_dir + '/' + one_dir + '/label/' + one_label, root_dir + '/all/label/' + one_label)

def move_from_all(root_dir):
	ignore_list = ['OK', '区域色差_部分', '小目标_清晰点', '正常元素_延伸光滑', '毛刺_孔', '金面_较清晰', '防焊_模糊', 'all', 'all_src']
	root_all_source_dir = root_dir + '/all_src/source'
	root_all_label_dir = root_dir + '/all_src/label'
	for one_dir in os.listdir(root_dir):
		if one_dir not in ignore_list:
			for one_source in os.listdir(root_dir + '/' + one_dir + '/source'):
				shutil.copy(root_all_source_dir + '/' + one_source, root_dir + '/' + one_dir + '/source/' + one_source)
			for one_label in os.listdir(root_dir + '/' + one_dir + '/label'):
				shutil.copy(root_all_label_dir + '/' + one_label, root_dir + '/' + one_dir + '/label/' + one_label)


def split_set(all_root_dir, single_set_dir, dst_root_dir):
	if not os.path.exists(dst_root_dir + '/test/source'):
		os.makedirs(dst_root_dir + '/test/source')
	if not os.path.exists(dst_root_dir + '/test/label'):
		os.makedirs(dst_root_dir + '/test/label')
	if not os.path.exists(dst_root_dir + '/train/source'):
		os.makedirs(dst_root_dir + '/train/source')
	if not os.path.exists(dst_root_dir + '/train//label'):
		os.makedirs(dst_root_dir + '/train/label')
	single_set_list = []
	for one_file in os.listdir(single_set_dir):
		single_set_list.append(one_file.strip().split('.')[0])
	all_source_dir = all_root_dir + '/source'
	for one_source in os.listdir(all_source_dir):
		one_source_path = all_source_dir + '/' + one_source
		one_label_path = all_root_dir + '/label/' + one_source.strip().split('.')[0] + '.aqlabel'
		if one_source.strip().split('.')[0] in single_set_list:
			dst_one_source_path = dst_root_dir + '/test/source/' + one_source
			dst_one_label_path = dst_root_dir + '/test/label/' + one_source.strip().split('.')[0] + '.aqlabel'
		else:
			dst_one_source_path = dst_root_dir + '/train/source/' + one_source
			dst_one_label_path = dst_root_dir + '/train/label/' + one_source.strip().split('.')[0] + '.aqlabel'		
		shutil.copy(one_source_path, dst_one_source_path)
		shutil.copy(one_label_path, dst_one_label_path)

def split_set_json(all_root_dir, single_set_dir, dst_root_dir):
	if not os.path.exists(dst_root_dir + '/test/source'):
		os.makedirs(dst_root_dir + '/test/source')
	if not os.path.exists(dst_root_dir + '/test/label'):
		os.makedirs(dst_root_dir + '/test/label')
	if not os.path.exists(dst_root_dir + '/train/source'):
		os.makedirs(dst_root_dir + '/train/source')
	if not os.path.exists(dst_root_dir + '/train//label'):
		os.makedirs(dst_root_dir + '/train/label')
	single_set_list = []
	for one_file in os.listdir(single_set_dir):
		single_set_list.append(one_file.strip().split('.')[0])
	all_source_dir = all_root_dir + '/source'
	for one_source in os.listdir(all_source_dir):
		one_source_path = all_source_dir + '/' + one_source
		one_label_path = all_root_dir + '/label/' + one_source.strip().split('.')[0] + '.json'
		if one_source.strip().split('.')[0] in single_set_list:
			dst_one_source_path = dst_root_dir + '/test/source/' + one_source
			dst_one_label_path = dst_root_dir + '/test/label/' + one_source.strip().split('.')[0] + '.json'
		else:
			dst_one_source_path = dst_root_dir + '/train/source/' + one_source
			dst_one_label_path = dst_root_dir + '/train/label/' + one_source.strip().split('.')[0] + '.json'		
		shutil.copy(one_source_path, dst_one_source_path)
		shutil.copy(one_label_path, dst_one_label_path)

def aidi_list(root_dir):
	source_dir = root_dir + '/source'
	label_dir = root_dir + '/label'
	res = []
	for one_source in os.listdir(source_dir):
		number = one_source.strip().split('.')[0]
		one_label = number + '.aqlabel'
		if one_label in os.listdir(label_dir):
			res.append(number)
	return res

		

def re_arrange(root_dir,dst_root_dir):
	train_source_dir = root_dir + '/train/source'
	train_label_dir = root_dir + '/train/label'
	test_source_dir = root_dir + '/test/source'
	test_label_dir = root_dir + '/test/label'
	if not os.path.exists(dst_root_dir + '/source'):
		os.makedirs(dst_root_dir + '/source')
	if not os.path.exists(dst_root_dir + '/label'):
		os.makedirs(dst_root_dir + '/label')
	count = 1
	for one_source in os.listdir(train_source_dir):
		src_source_path = train_source_dir + '/' + one_source
		src_label_path = train_label_dir + '/' + one_source.split('.')[0] + '.aqlabel'
		dst_source_path = dst_root_dir + '/source/' + str(count) + '.aqimg'
		dst_label_path = dst_root_dir + '/label/' + str(count) + '.aqlabel'
		shutil.copy(src_source_path, dst_source_path)
		shutil.copy(src_label_path, dst_label_path)
		count = count + 1

	for one_source in os.listdir(test_source_dir):
		src_source_path = test_source_dir + '/' + one_source
		src_label_path = test_label_dir + '/' + one_source.split('.')[0] + '.aqlabel'
		dst_source_path = dst_root_dir + '/source/' + str(count) + '.aqimg'
		dst_label_path = dst_root_dir + '/label/' + str(count) + '.aqlabel'
		shutil.copy(src_source_path, dst_source_path)
		shutil.copy(src_label_path, dst_label_path)
		count = count + 1

def re_arrange2(root_dir,dst_root_dir):
	train_source_dir = root_dir + '/source'
	train_label_dir = root_dir + '/label'

	if not os.path.exists(dst_root_dir + '/source'):
		os.makedirs(dst_root_dir + '/source')
	if not os.path.exists(dst_root_dir + '/label'):
		os.makedirs(dst_root_dir + '/label')

	if not os.path.exists(dst_root_dir + '/source_test'):
		os.makedirs(dst_root_dir + '/source_test')
	if not os.path.exists(dst_root_dir + '/label_test'):
		os.makedirs(dst_root_dir + '/label_test')
	count = 1
	source_list = os.listdir(train_source_dir)
	choose_num = int(len(source_list) * 0.7)

	while len(source_list) > 0:
		num = int(random.random() * len(source_list))		
		one_source = source_list[num]
		source_list.pop(num)

		if count < choose_num + 1:
			src_source_path = train_source_dir + '/' + one_source
			src_label_path = train_label_dir + '/' + one_source.split('.')[0] + '.aqlabel'
			dst_source_path = dst_root_dir + '/source/' + str(count) + '.png'
			dst_label_path = dst_root_dir + '/label/' + str(count) + '.aqlabel'
			shutil.copy(src_source_path, dst_source_path)
			shutil.copy(src_label_path, dst_label_path)
		else:
			src_source_path = train_source_dir + '/' + one_source
			src_label_path = train_label_dir + '/' + one_source.split('.')[0] + '.aqlabel'
			dst_source_path = dst_root_dir + '/source_test/' + str(count) + '.png'
			dst_label_path = dst_root_dir + '/label_test/' + str(count) + '.aqlabel'
			shutil.copy(src_source_path, dst_source_path)
			shutil.copy(src_label_path, dst_label_path)

		count = count + 1


def re_arrange_json(root_dir,dst_root_dir):
	train_source_dir = root_dir + '/train/source'
	train_label_dir = root_dir + '/train/label'
	test_source_dir = root_dir + '/test/source'
	test_label_dir = root_dir + '/test/label'
	if not os.path.exists(dst_root_dir + '/source'):
		os.makedirs(dst_root_dir + '/source')
	if not os.path.exists(dst_root_dir + '/label'):
		os.makedirs(dst_root_dir + '/label')
	count = 1
	for one_source in os.listdir(train_source_dir):
		src_source_path = train_source_dir + '/' + one_source
		src_label_path = train_label_dir + '/' + one_source.split('.')[0] + '.json'
		dst_source_path = dst_root_dir + '/source/' + str(count) + '.xml'
		dst_label_path = dst_root_dir + '/label/' + str(count) + '.json'
		shutil.copy(src_source_path, dst_source_path)
		shutil.copy(src_label_path, dst_label_path)
		count = count + 1

	for one_source in os.listdir(test_source_dir):
		src_source_path = test_source_dir + '/' + one_source
		src_label_path = test_label_dir + '/' + one_source.split('.')[0] + '.json'
		dst_source_path = dst_root_dir + '/source/' + str(count) + '.xml'
		dst_label_path = dst_root_dir + '/label/' + str(count) + '.json'
		shutil.copy(src_source_path, dst_source_path)
		shutil.copy(src_label_path, dst_label_path)
		count = count + 1

def choose_class(source_dir,aqlabel_dir,json_dir,dst_root_dir):

	class_3_list = ['小铜孔毛刺','文字块异物','大焊盘粘胶','基材孔上铜','小焊盘氧化','数字焊盘粘胶','大焊盘异物','焊盘露铜',
	'小焊盘污染','数字焊盘异物','板损','防焊脱落','小焊盘刮伤','孔环焊盘异物','小焊盘渗金','防焊假漏','塞孔沾金','孔环焊盘氧化','线路沾金',
	'防焊发白','焊盘针孔压伤','孔环焊盘污染','线路露铜','大焊盘渗金','焊盘可移动异物','孔环焊盘露镍','线路假漏','BGA焊盘异物','大焊盘氧化',
	'金属毛刺','文字上盘','BGA焊盘污染','大焊盘污染','非金属毛刺','文字块污染','文字线条残缺','大焊盘露镍','防焊杂质','文字残缺','防焊上数字焊盘',
	'小焊盘粘胶','防焊污染','数字焊盘污染','防焊刮伤','小焊盘异物','防焊露铜','孔环焊盘粘胶','大焊盘刮伤','小焊盘露镍','防焊可移动异物','孔环焊盘缺损',
	'线路杂质','大铜孔毛刺','孔环焊盘刮伤']
	class_2_list = ['防焊上焊盘','小铜孔堵塞异物','文字反沾','焊盘凸起凹陷']
	class_1_list = ['散热孔堵塞异物','焊盘曝虚','防焊沾金','文字漏印','少加工','漏塞孔','多加工','掉绿油桥','大铜孔堵塞异物','文字印错',
	'焊盘曝偏','塞孔假漏','孔环焊盘曝偏','背钻孔堵塞异物']
	class_0_list = ['OK']

	target_class = class_3_list

	if not os.path.exists(dst_root_dir + '/class_1/source'):
		os.makedirs(dst_root_dir + '/class_1/source')
	if not os.path.exists(dst_root_dir + '/class_1/label'):
		os.makedirs(dst_root_dir + '/class_1/label')

	if not os.path.exists(dst_root_dir + '/class_2/source'):
		os.makedirs(dst_root_dir + '/class_2/source')
	if not os.path.exists(dst_root_dir + '/class_2/label'):
		os.makedirs(dst_root_dir + '/class_2/label')

	if not os.path.exists(dst_root_dir + '/class_3/source'):
		os.makedirs(dst_root_dir + '/class_3/source')
	if not os.path.exists(dst_root_dir + '/class_3/label'):
		os.makedirs(dst_root_dir + '/class_3/label')

	if not os.path.exists(dst_root_dir + '/class_0/source'):
		os.makedirs(dst_root_dir + '/class_0/source')
	if not os.path.exists(dst_root_dir + '/class_0/label'):
		os.makedirs(dst_root_dir + '/class_0/label')

	for one_json in os.listdir(json_dir):
		json_str = open(os.path.join(json_dir,one_json),'r', encoding='UTF-8')
		json_dict = json.load(json_str)
		class_name = json_dict[0]['label']

		index = one_json.strip().split('.')[0]
		one_source_src_path = source_dir + '/' + index + '.aqimg'
		one_label_src_path = aqlabel_dir + '/' + index + '.aqlabel'


		if class_name in class_1_list:
			one_source_dst_path = dst_root_dir + '/class_1/source/' + index + '.aqimg'
			one_label_dst_path = dst_root_dir + '/class_1/label/' + index + '.aqlabel'
			shutil.copy(one_source_src_path, one_source_dst_path)
			shutil.copy(one_label_src_path, one_label_dst_path)
		elif class_name in class_2_list:
			one_source_dst_path = dst_root_dir + '/class_2/source/' + index + '.aqimg'
			one_label_dst_path = dst_root_dir + '/class_2/label/' + index + '.aqlabel'
			shutil.copy(one_source_src_path, one_source_dst_path)
			shutil.copy(one_label_src_path, one_label_dst_path)	
		elif class_name in class_3_list:
			one_source_dst_path = dst_root_dir + '/class_3/source/' + index + '.aqimg'
			one_label_dst_path = dst_root_dir + '/class_3/label/' + index + '.aqlabel'
			shutil.copy(one_source_src_path, one_source_dst_path)
			shutil.copy(one_label_src_path, one_label_dst_path)
		elif class_name in class_0_list:
			one_source_dst_path = dst_root_dir + '/class_0/source/' + index + '.aqimg'
			one_label_dst_path = dst_root_dir + '/class_0/label/' + index + '.aqlabel'
			shutil.copy(one_source_src_path, one_source_dst_path)
			shutil.copy(one_label_src_path, one_label_dst_path)
		else:
			print(class_name,index)


def make_list(root_dir,out_dir):
	fp=open(out_dir,'w')
	print(root_dir)

	for one_source in os.listdir(root_dir):
		print(one_source)
		one_source_path = root_dir + '/' + one_source
		fp.write(one_source_path)
		fp.write('\n')  

		


	
		

if __name__ == '__main__':
	# copy_files()
	# json_dir = './Reg_Project0529_1/RegClassify_0/label'
	# source_source_dir = './label0725_test_classify7/RegClassify_0/source'
	# source_label_dir = './label0725_test_classify7/RegClassify_0/label'
	# target_root_dir = './classify_with_json0813'
	# # copy_files_with_json(json_dir,source_source_dir,source_label_dir,target_root_dir)
	# analysis_display(target_root_dir)
	# analysis_display('./select0812')
	# label_intersection('F:/yang.xie/aidi/class0808/class0808_label/class0808_class_train/Segment_0/label','F:/yang.xie/aidi/label0725/train0814/all/label','./label_tmp')
	
	# source_dir = 'F:/yang.xie/aidi/big6000_0817/select_train0814_xy/基础三类/3_train'
	# label_src = 'F:/yang.xie/aidi/big6000_0817/select_train0814_xy/基础三类/label'
	# label_dst = 'F:/yang.xie/aidi/big6000_0817/select_train0814_xy/基础三类/label_find'
	# find_label(source_dir, label_src, label_dst)
	
	
	# analysis_display('./select_train_add_label')
	# analysis_display('./select_test_add_label')
	# move_to_all('./select_test_add_label')
	# move_from_all('./select_test_add_label')

	# display_json('./origin_data/label_json')

	# all_root_dir = 'F:/yang.xie/aidi/big9000_0820/copy_project_classify_use/RegClassify_0'
	# single_set_dir = 'F:/yang.xie/aidi/test9000_0828/xbq-b2/RegClassify_0/label'
	# dst_root_dir = './split_set'
	# split_set(all_root_dir, single_set_dir, dst_root_dir)

	# root_dir = './split_set'
	# dst_root_dir = './re_arrange'
	# re_arrange(root_dir,dst_root_dir)

	# all_dir = './classify_8_25_0812'
	# train_dir = './select_train_add_label'
	# test_dir = './select_test_add_label'
	# select_test_set(all_dir, train_dir, test_dir)

	# all_root_dir = 'D:/yang.xie/aidi_projects/xbq-b/RegClassify_0'
	# single_set_dir = 'D:/yang.xie/aidi_projects/split_set/test/source'
	# dst_root_dir = './split_set_json'
	# split_set_json(all_root_dir, single_set_dir, dst_root_dir)

	# dst_root_dir2 = './re_arrange_json'
	# re_arrange_json(dst_root_dir,dst_root_dir2)

		# root_dir = './split_set'
	# dst_dir = '../task_9000_rearrange_new'
	# re_arrange(root_dir,dst_dir)

	# tmp = []
	# for i in range(1,6820):
	# 	tmp.append(i)
	# print(tmp)

	# source_dir = 'F:/yang.xie/aidi_projects/big9000_0820/origin_data/source'
	# aqlabel_dir = 'F:/yang.xie/aidi_projects/big9000_0820/origin_data/label'
	# json_dir = 'F:/yang.xie/aidi_projects/big9000_0820/origin_data/label_json'
	# dst_root_dir = 'F:/yang.xie/aidi_projects/reg_classify0909/origin_data'
	# choose_class(source_dir,aqlabel_dir,json_dir,dst_root_dir)

	# root_dir = "./origin_data"
	# dst_dir = "./classify_single"

	# re_arrange2(root_dir,dst_dir)

	# target_dir = 'class_2'
	# root_dir = 'F:/yang.xie/aidi_projects/reg_classify0909/origin_data/' + target_dir + '/source'
	# out_dir = target_dir + '_list.txt'
	# make_list(root_dir,out_dir)






					



