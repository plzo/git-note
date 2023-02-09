import os
import sys
import random,shutil



def find_label(label_dir, image_src, image_dst):
	if not os.path.exists(image_dst):
		os.makedirs(image_dst)
	for one_source in os.listdir(label_dir):
		one_img = one_source.split('.')[0] + '.aqimg'
		shutil.copy(image_src + '/' + one_img, image_dst + '/' + one_img)

if __name__ == '__main__':

	label_dir = r'D:\yang.xie\aidi_projects\20210731-debug\data0823\label'
	image_src = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\pcb_origin_iter04\RegClassify_0\source'
	image_dst = r'D:\yang.xie\aidi_projects\20210731-debug\data0823\source'
	find_label(label_dir, image_src, image_dst)

