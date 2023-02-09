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

def trans_index_db(root_dir):
    train_list = get_list(root_dir,'train')
    new_train_list = []
    for one in train_list:
        new_train_list.append(int(one) + 10000000)
    print(new_train_list)

def trans_index_task(json_path):
    task_json_str = open(json_path,'r', encoding='UTF-8')
    task_json_dict = json.load(task_json_str)
    train_list = task_json_dict['indexes']['value']
    new_train_list = []
    for one in train_list:
        new_train_list.append(int(one) + 10000000)
    print(new_train_list)


if __name__ == '__main__':
    root_dir = r'F:\yang.xie\projects\20211115_chaosheng\adc_train1214\Classify_0'
    json_path = r'F:\yang.xie\projects\20211115_chaosheng\adc_train1214\Classify_0\test_task.json'
    # trans_index_db(project_dir)
    trans_index_task(json_path)









