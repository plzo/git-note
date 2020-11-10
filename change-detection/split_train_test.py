import os
import sys
import shutil
import json
import random


def copy_set(src_dir,std_dir,dst_dir):
	if not os.path.exists(dst_dir):
		os.makedirs(dst_dir)
	for one_source in os.listdir(std_dir):
		one_label = one_source.split('.')[0] + '.aqlabel'
		shutil.move(src_dir + '/' + one_label, dst_dir + '/' + one_label)	

if __name__ == '__main__':
	src_dir = 'D:/yang.xie/aidi_projects/project-20201022/classify_no_reg/Classify_0/label'
	std_dir = 'D:/yang.xie/aidi_projects/project-20201022/data/训练集/source'
	dst_dir = 'D:/yang.xie/aidi_projects/project-20201022/data/训练集_程度/label'
	copy_set(src_dir,std_dir,dst_dir)
	





					



