import os
import sys
import shutil
import json
import random


def move_test(src_dir,dst_dir):
	for one_label in os.listdir(src_dir):
		src_label_path = src_dir + '/' + one_label
		dst_label_path = dst_dir + '/' + one_label
		shutil.move(src_label_path, dst_label_path)
	
		

if __name__ == '__main__':
	src_dir = './select_test_label'
	dst_dir = './label'
	move_test(src_dir,dst_dir)
	





					



