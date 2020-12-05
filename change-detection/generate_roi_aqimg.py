import os
import sys
import cv2
import json
import shutil
import random
import numpy as np

sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *


def get_random_set():
    points = []
    image_size = [128,128]
    x = image_size[0]/2
    y = image_size[1]/2
    w = x*random.random()
    h = y*random.random()
    points.append([[x-w/2,y-h/2]])
    points.append([[x-w/2,y+h/2]])
    points.append([[x+w/2,y+h/2]])
    points.append([[x+w/2,y-h/2]])

    return [points]

def insert_mat(in_path,out_path,mat):

    img = Image()
    img_out = Image()
    img.from_file(in_path)
    roi_aqimg = numpy2image(mat)
    batch_img = BatchImage([img.visual_at(0),img.visual_at(1), roi_aqimg])
    img_out.from_batch(batch_img)
    img_out.to_file(out_path)

# def insert_mat(in_path,out_path,mat):
    # img = Image()
    # img.from_file(in_path)
    # mat_img = image2numpy(img)
    # defect_img = image2numpy(img.visual_at(0))
    # origin_img = image2numpy(img.visual_at(1))
    # roi_img = generate_random_mat()
    # merge_img = cv2.merge((defect_img,origin_img,roi_img))
    # merge_aqimg = numpy2image(merge_img)
    # merge_aqimg.to_file(out_path)
    # print(merge_aqimg.visual_size())


def get_points_set(one_label_path):
    in_label = LabelIO()
    in_label.read_from(one_label_path)
    json_label = json.loads(in_label.to_json())
    points_set = []
    for one_region in json_label['regions']:
        points = []
        for one_point in one_region['polygon']['outer']['points']:
            points.append([[one_point['x'],one_point['y']]])
        points_set.append(points)
    return points_set


def generate_mat(points_set):
    mat = 255*np.ones((128,128),dtype=np.uint8)
    contours = np.array(points_set).astype(np.int32)
    cv2.drawContours(mat,contours,-1,0,-1)
    dst = cv2.distanceTransform(mat,cv2.DIST_L2, 3).astype(np.uint8)
    dst_merge = cv2.merge((dst,dst,dst))

    # cv2.imshow('img',mat)
    # cv2.waitKey(0)
    # cv2.imshow('img',dst)
    # cv2.waitKey(0)
    return dst_merge


def generate_aqimg_roi(aqimg_roi_dir,aqimg_dir,label_dir = ''):
    if not os.path.exists(aqimg_roi_dir):
        os.makedirs(aqimg_roi_dir)
    for one_aqimg in os.listdir(aqimg_dir):
        dst_path = aqimg_roi_dir + '/' + one_aqimg
        src_path = aqimg_dir + '/' + one_aqimg
        if label_dir == '':
            insert_mat(src_path,dst_path,generate_mat(get_random_set()))
        else:
            label_path = label_dir + '/' + one_aqimg.split('.')[0] + '.aqlabel'
            # generate_mat(get_points_set(label_path))
            insert_mat(src_path,dst_path,generate_mat(get_points_set(label_path)))


if __name__ == '__main__':
    label_dir = r'D:\yang.xie\aidi_projects\20201203-ROI-bias\generate_label\Detection_0\label'
    aqimg_dir = r'D:\yang.xie\aidi_projects\20201203-ROI-bias\generate_label\Detection_0\source'
    aqimg_roi_dir = r'D:\yang.xie\aidi_projects\20201203-ROI-bias\generate_label\Detection_0\source_roi'
    
    aqimg_ok_dir = r'D:\yang.xie\aidi_projects\20201203-ROI-bias\generate_label\Detection_0\source_ok'
    aqimg_ok_roi_dir = r'D:\yang.xie\aidi_projects\20201203-ROI-bias\generate_label\Detection_0\source_ok_roi'

    # generate_aqimg_roi(aqimg_roi_dir,aqimg_dir,label_dir)
    # generate_aqimg_roi(aqimg_ok_roi_dir,aqimg_ok_dir)




