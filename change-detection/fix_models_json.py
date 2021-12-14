import os
import sys
import shutil
import json
import random


def fix_models(models_dir):
	models_dict = {}
	models_list = []
	for one_dir in os.listdir(models_dir):
		one_path = models_dir + '\\' + one_dir
		if os.path.isdir(one_path):
			one_dict = {}
			one_dict['key'] = one_dir
			one_dict['value'] = one_path
			models_list.append(one_dict)
	models_dict['datas'] = models_list
	json.dump(models_dict, open(models_dir + '/models.json', 'w',encoding='UTF-8'),ensure_ascii=False)	

	
if __name__ == '__main__':
	models_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\pcb_origin_iter04_cp\RegClassify_0\models\origin0913'
	fix_models(models_dir)


		





					



