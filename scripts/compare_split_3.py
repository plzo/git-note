import os
import sys
import shutil
import json
import random

def compare_split(dir1,dir2,out_dir):
	only_dir1 = out_dir + '/only_dir1'
	only_dir2 = out_dir + '/only_dir2'
	both = out_dir + '/both'
	if not os.path.exists(only_dir1):
		os.makedirs(only_dir1)
	if not os.path.exists(only_dir2):
		os.makedirs(only_dir2)
	if not os.path.exists(both):
		os.makedirs(both)

	for one_file in os.listdir(dir1):
		if one_file in os.listdir(dir2):
			shutil.copy(dir1 + '/' + one_file, both + '/' + one_file)
		else:
			shutil.copy(dir1 + '/' + one_file, only_dir1 + '/' + one_file)
	for one_file in os.listdir(dir2):
		if one_file not in os.listdir(dir1):
			shutil.copy(dir2 + '/' + one_file, only_dir2 + '/' + one_file)

if __name__ == '__main__':
	dir1 = 'D:/yang.xie/aidi_projects/update-label0918/compare_tmp/all_concat_error/source'
	dir2 = 'D:/yang.xie/aidi_projects/update-label0918/compare_tmp/all_minus_error/source'
	out_dir = 'D:/yang.xie/aidi_projects/update-label0918/compare_tmp/res'
	compare_split(dir1,dir2,out_dir)
	





					



