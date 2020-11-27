import os
import sys
import random,shutil



def find_label(source_dir, label_src, label_dst):
	if not os.path.exists(label_dst):
		os.makedirs(label_dst)
	for one_source in os.listdir(source_dir):
		one_label = one_source.split('.')[0] + '.aqlabel'
		shutil.copy(label_src + '/' + one_label, label_dst + '/' + one_label)

if __name__ == '__main__':

	# source_dir = 'D:/yang.xie/aidi_projects/project-20201022/5_cls/RegClassify_0/source'
	# label_src = 'D:/yang.xie/aidi_projects/project-20201022/base_project/RegClassify_0/label'
	# label_dst = 'D:/yang.xie/aidi_projects/project-20201022/5_cls/RegClassify_0/label'
	
	source_dir = 'D:/yang.xie/aidi_projects/20201117-iteration4/iter04/train_set/source'
	label_src = 'D:/yang.xie/aidi_projects/20201117-iteration4/iter04/RegClassify_0/label'
	label_dst = 'D:/yang.xie/aidi_projects/20201117-iteration4/iter04/train_set/label'
	find_label(source_dir, label_src, label_dst)

