import os
import sys
import cv2
import json
import shutil
import random
import numpy as np

sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *

def get_points_set(one_label_path):
    in_label = LabelIO()
    in_label.read_from(one_label_path)
    json_label = json.loads(in_label.to_json())
    points_set = []
    for one_region in json_label['regions']:
        points = []
        for one_point in one_region['polygon']['outer']['points']:
            points.append([one_point['x'],one_point['y']])
        points_set.append(points)
    return points_set[0]

def get_roi(points_set):
    min_x = points_set[0][0]
    max_x = points_set[0][0]
    min_y = points_set[0][1]
    max_y = points_set[0][1]
    for one_point in points_set:
        min_x = min(min_x,one_point[0])
        max_x = max(max_x,one_point[0])
        min_y = min(min_y,one_point[1])
        max_y = max(max_y,one_point[1])
    return [min_y,max_y,min_x,max_x]


def crop_dir(project_dir):
    source_dir = project_dir + '/source'
    label_dir = project_dir + '/label-roi'
    dst_dir = project_dir + '/source-roi-resize128'
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for one_label in os.listdir(label_dir):
        one_label_path = label_dir + '/' + one_label
        points_set = get_points_set(one_label_path)
        roi = get_roi(points_set)
        one_img_path = source_dir + '/' + one_label.split('.')[0] + '.png'
        one_img_dst_path = dst_dir + '/' + one_label.split('.')[0] + '.png'
        img = cv2.imread(one_img_path)
        img = img[int(roi[0]):int(roi[1]),int(roi[2]):int(roi[3])]
        dim = (128, 128)
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        cv2.imwrite(one_img_dst_path,resized)      




if __name__ == '__main__':
    project_dir = r'D:\yang.xie\aidi_projects\20210105-multi-cls\cls2\Classify_0'
    crop_dir(project_dir)







