import os
import sys
import random,shutil

root_path='F:/yang.xie/data/change_detection'
output_path='./change_detection_out_put'

train_count_label = 1
train_count_source = 1
test_count_label = 1
test_count_source = 1
def label_move(label_path,num):
	global train_count_label
	global test_count_label
	i = 1
	for label_file in os.listdir(label_path):
		file_path = label_path + '/' + label_file
		if i < num + 1:
			dst_path = output_path + '/trainset/label/' + str(train_count_label) + '.aqlabel'
			shutil.copy(file_path,dst_path)
			train_count_label = train_count_label + 1
		else:
			dst_path = output_path + '/testset/label/' + str(test_count_label) + '.aqlabel'
			shutil.copy(file_path,dst_path)
			test_count_label = test_count_label + 1
		i = i + 1

def source_move(source_path,num):
	global train_count_source
	global test_count_source
	i = 1
	for source_file in os.listdir(source_path):
		file_path = source_path + '/' + source_file
		if i < num + 1:
			dst_path = output_path + '/trainset/source/' + str(train_count_source) + '.aqimg'
			shutil.copy(file_path,dst_path)
			train_count_source = train_count_source + 1
		else:
			dst_path = output_path + '/testset/source/' + str(test_count_source) + '.aqimg'
			shutil.copy(file_path,dst_path)
			test_count_source = test_count_source + 1
		i = i + 1	

for subdir1 in os.listdir(root_path):
	subdir1_path = root_path+'/'+subdir1
	if os.path.isdir(subdir1_path):
		for subdir2 in os.listdir(subdir1_path):
			subdir2_path = subdir1_path + '/' + subdir2 + '/Segment_0'
			label_path = subdir2_path + '/label'
			source_path = subdir2_path + '/source'
			if subdir2 == 'heihuihuashang_qingdu_seg':
				label_move(label_path,97)
				source_move(source_path,97)
			elif subdir2 == 'heihuihuashang_yanzhong_seg':
				label_move(label_path,40)
				source_move(source_path,40)
			elif subdir2 == 'heihuihuashang_zhongdu_seg':
				label_move(label_path,73)
				source_move(source_path,73)
			elif subdir2 == 'jinshuyanghua_qingdu_seg':
				label_move(label_path,86)
				source_move(source_path,86)
			elif subdir2 == 'jinshuyanghua_yanzhong_seg':
				label_move(label_path,50)
				source_move(source_path,50)
			elif subdir2 == 'jinshuyanghua_zhongdu_seg':
				label_move(label_path,74)
				source_move(source_path,74)
			if subdir2 == 'xiaohanpanyiwu_qingdu_seg':
				label_move(label_path,24)
				source_move(source_path,24)
			elif subdir2 == 'xiaohanpanyiwu_yanzhong_seg':
				label_move(label_path,136)
				source_move(source_path,136)
			elif subdir2 == 'xiaohanpanyiwu_zhongdu_seg':
				label_move(label_path,50)
				source_move(source_path,50)
			elif subdir2 == 'TEST':
				label_move(label_path,210)
				source_move(source_path,210)
			else:
				continue


					



