import os
import sys
import cv2
import json
import shutil
import numpy as np
import sqlite3

sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *


def get_name_score(one_label_path):
    if one_label_path.endswith('json'):
        with open(one_label_path, 'r', encoding='utf8') as fp:
            json_data = json.load(fp)
            return json_data[0]['label']
    else:
        in_label = LabelIO()
        in_label.read_from(one_label_path)
        json_label = json.loads(in_label.to_json())
        return json_label['regions'][0]['name'], json_label['regions'][0]['score']


def get_db_file(root_dir):
    for one_file in os.listdir(root_dir + '/..'):
        if one_file.endswith('.db'):
            return root_dir + '/../' + one_file
    print('Can not find db file!')
    return ''


def get_list(root_dir,eval_set):
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
        return [row[0] for row in cursor]

global_miss_list = []

def judge_one(one_label,one_label_path,prob_dirs):
    label_name,label_score = get_name_score(one_label_path)
    probs_name = 'OK'
    probs_score = 0.99
    for prob_dir in prob_dirs:
        prob_path = prob_dir + '/' + one_label
        prob_name,prob_score = get_name_score(prob_path)
        print('channel: ',prob_dir.split('_')[-1],'  label: ',label_name,'  prob: ',prob_name,'  score: ',prob_score)
        if prob_name != 'OK':
            if probs_name == 'OK':
                probs_name = prob_name
                probs_score = prob_score
            else:
                if prob_score > probs_score:
                    probs_name = prob_name
                    probs_score = prob_score
        else:
            if probs_name == 'OK' and prob_score < probs_score:
                probs_score = prob_score
        global global_miss_list

        if label_name != 'OK' and prob_name == 'OK':
            global_miss_list.append(int(one_label.split('.')[0]))


    # if probs_name == 'OK' and probs_score < 0.98:
    #     probs_name = '绿油异物'
    
    if label_name == 'OK' and probs_name != 'OK':
        return 'over',probs_name,probs_score
    elif label_name != 'OK' and probs_name == 'OK':
        return 'miss',probs_name,probs_score
    else:
        return 'true',probs_name,probs_score

def change_label(project_dir,one_label,save_dir,name,score):
    json_path = project_dir + '/tmp.json'
    img_path = project_dir + '/source/' + one_label.split('.')[0] + '.aqimg'
    src_label_path = project_dir + '/label/' + one_label
    json_dict = [{'label':name,'score':score}]
    json.dump(json_dict, open(json_path, 'w',encoding='UTF-8'),ensure_ascii=False)
    out_label = LabelIO()
    read_33X_classify_label(json_path, img_path, out_label)
    save_path = save_dir + '/' + one_label
    out_label.save_to(save_path)

def classify_eval(project_dir,prob_dirs):
    train_list = get_list(project_dir,'train')
    test_list = get_list(project_dir,'test')
    label_dir = project_dir + '/label'
    save_dir = project_dir + '/combine_result'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    miss_list = []
    over_list = []
    miss_num = 0
    over_num = 0
    # eval_list = test_list
    eval_list = [110, 115, 1973, 1973, 1973, 1973, 1976, 2019, 2019, 2019, 2019, 2019, 2338, 2345, 2345, 2345, 2345, 2345, 2345, 2345, 2345, 3326, 3326, 3326, 3326, 3326, 3547, 3547, 3547, 3547, 3547, 3547, 3547, 4130, 4130, 4130, 4130, 4130, 4130, 4130, 4142, 4435, 4435, 4435, 4435, 4435, 4435, 4435, 4435, 5265, 5265, 5265, 6844, 6844, 7457, 7457, 7457, 8685, 8685, 8685, 8950, 8982, 9003, 9255, 9255, 9255, 9305, 9305, 9385, 9385, 9855, 9855, 9855, 9855, 9855, 9855]
    for one_label in os.listdir(label_dir):
        if int(one_label.split('.')[0]) in eval_list:
            print('*****************',one_label,'*****************')
            one_label_path = label_dir + '/' + one_label
            res,name,score = judge_one(one_label,one_label_path,prob_dirs)

            if res == 'miss':
                miss_list.append(one_label_path)
                miss_num += 1
            elif res == 'over':
                over_list.append(one_label_path)
                over_num += 1
            change_label(project_dir,one_label,save_dir,name,score)
    print('miss_list: ')
    print(miss_list)
    print('over_list: ')
    print(over_list)
    print('miss_num: ',miss_num)
    print('over_num: ',over_num)
    global global_miss_list
    print(global_miss_list)





if __name__ == '__main__':
    channel_list = ['r','g','b','rgb','h','s','v','hsv']
    prob_dirs = []
    for channel in channel_list:
        prob_dir = 'D:/yang.xie/aidi_projects/20201222-rgbhs/cls_roi_' + channel + '/Classify_0/TEST_RESULTS/R102_1500_' + channel
        prob_dirs.append(prob_dir)
    
    project_dir = r'D:\yang.xie\aidi_projects\20201222-rgbhs\cls_roi_r\Classify_0'
    classify_eval(project_dir,prob_dirs)


