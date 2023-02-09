import os
import sys
import shutil
import json
import random

def select_test(label_dir,dst_dir):
	if not os.path.exists(dst_dir):
		os.makedirs(dst_dir)
	label_list = []
	for one_label in os.listdir(label_dir):
		index = int(one_label.strip().split('.')[0])
		if index < 100000:
			label_list.append(one_label)
	print(len(label_list))

	count = 1
	choose_num = int(len(label_list) * 0.3)
	while count < choose_num + 1:
		num = int(random.random() * len(label_list))		
		one_choose_label = label_list[num]
		one_choose_label_pair = str(int(one_choose_label.strip().split('.')[0]) + 100000) + '.aqlabel'
		label_list.pop(num)

		src_label_path = label_dir + '/' + one_choose_label
		dst_label_path = dst_dir + '/' + one_choose_label
		shutil.move(src_label_path, dst_label_path)
		src_label_path = label_dir + '/' + one_choose_label_pair
		dst_label_path = dst_dir + '/' + one_choose_label_pair
		shutil.move(src_label_path, dst_label_path)
		count = count + 1

			

if __name__ == '__main__':
	label_dir = './label'
	dst_dir = './select_test_label'
	select_test(label_dir,dst_dir)
	





					



