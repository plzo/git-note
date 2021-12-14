import os
import sys
import cv2
import json
import shutil
import sqlite3


def get_db_file(root_dir):
    for one_file in os.listdir(root_dir + '/..'):
        if one_file.endswith('.db'):
            return root_dir + '/../' + one_file
    print('Can not find db file!')
    return ''

def get_list(root_dir, eval_set):
    db_file = get_db_file(root_dir)			
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        if eval_set == 'train':
            try:
                cursor = c.execute("SELECT id FROM RegClassify_0 WHERE selected == 1")
            except:
                cursor = c.execute("SELECT id FROM Classify_0 WHERE selected == 1")
        else:
            try:
                cursor = c.execute("SELECT id FROM RegClassify_0 WHERE selected == 2")
            except:
                cursor = c.execute("SELECT id FROM Classify_0 WHERE selected == 2")
        set_list = [row[0] for row in cursor]
    return set_list

def fix_task_json(root_dir):
	task_json_str = open(root_dir + '/task.json','r', encoding='UTF-8')
	task_json_dict = json.load(task_json_str)
	tmp_dict = task_json_dict
	# json.dump(tmp_dict, open(root_dir + '/task_bak.json', 'w',encoding='UTF-8'),ensure_ascii=False)
	task_json_dict['indexes']['value'] = get_list(root_dir,'train')
	task_json_dict['root_path']['value'] = root_dir
	json.dump(task_json_dict, open(project_dir + '/train_task.json', 'w',encoding='UTF-8'),ensure_ascii=False)
	task_json_dict['indexes']['value'] = get_list(root_dir,'test')
	json.dump(task_json_dict, open(project_dir + '/test_task.json', 'w',encoding='UTF-8'),ensure_ascii=False)

if __name__ == '__main__':
	project_dir = r'F:\yang.xie\projects\20211115_data_view\chaosheng_roi_aidi\Classify_0'
	fix_task_json(project_dir)








