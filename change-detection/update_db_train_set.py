import os
import sys
import sqlite3
import json

def get_db_file(project_dir):
    for one_file in os.listdir(project_dir + '/..'):
        if one_file.endswith('.db'):
            return project_dir + '/../' + one_file
    print('Can not find db file!')
    return ''

def update_db(project_dir):
    task_path = project_dir + '/task.json'
    task_json_str = open(task_path,'r', encoding='UTF-8')
    task_json_dict = json.load(task_json_str)
    train_list = task_json_dict['indexes']['value']
    moudle = project_dir.split('\\')[-1]

    with sqlite3.connect(get_db_file(project_dir)) as conn:
        c = conn.cursor()
        for one_index in train_list:
            cmd = "UPDATE " + moudle + " SET selected = 1 WHERE id == " + str(one_index)
            cursor = c.execute(cmd)
    print('finish!')

if __name__ == '__main__':
    project_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\test_sql\Classify_0'    
    update_db(project_dir)

