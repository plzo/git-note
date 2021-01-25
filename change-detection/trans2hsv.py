import os
import sys
import cv2
import json
import shutil
import numpy as np

sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *


def show(src_path,one_index):
        img = Image()
        img.from_file(src_path)
        defect_img = image2numpy(img.visual_at(0))
        hsv = cv2.cvtColor(defect_img, cv2.COLOR_BGR2HSV)
        H,S,V = cv2.split(hsv)
        R,G,B = cv2.split(defect_img)
        cv2.imwrite('../'+str(one_index)+'-01HSV.png', hsv)
        cv2.imwrite('../'+str(one_index)+'-02H.png', H)
        cv2.imwrite('../'+str(one_index)+'-03S.png', S)
        cv2.imwrite('../'+str(one_index)+'-04V.png', V)

        cv2.imwrite('../'+str(one_index)+'-05RGB.png', defect_img)
        cv2.imwrite('../'+str(one_index)+'-06R.png', R)
        cv2.imwrite('../'+str(one_index)+'-07G.png', G)
        cv2.imwrite('../'+str(one_index)+'-08B.png', B)
        
        # cv2.imshow('HSV1', hsv)
        # cv2.waitKey(0)

        # cv2.imshow('H2', H)
        # cv2.waitKey(0)

        # cv2.imshow('S3', S)
        # cv2.waitKey(0)

        # cv2.imshow('V4', V)
        # cv2.waitKey(0)

        origin_img = image2numpy(img.visual_at(1))
        hsv = cv2.cvtColor(origin_img, cv2.COLOR_BGR2HSV)
        R,G,B = cv2.split(origin_img)
        H,S,V = cv2.split(hsv)
        cv2.imwrite('../'+str(one_index)+'-09HSV.png', hsv)
        cv2.imwrite('../'+str(one_index)+'-10H.png', H)
        cv2.imwrite('../'+str(one_index)+'-11S.png', S)
        cv2.imwrite('../'+str(one_index)+'-12V.png', V)

        cv2.imwrite('../'+str(one_index)+'-13RGB.png', origin_img)
        cv2.imwrite('../'+str(one_index)+'-14R.png', R)
        cv2.imwrite('../'+str(one_index)+'-15G.png', G)
        cv2.imwrite('../'+str(one_index)+'-16B.png', B)
        
        # cv2.imshow('HSV5', hsv)
        # cv2.waitKey(0)

        # cv2.imshow('H6', H)
        # cv2.waitKey(0)

        # cv2.imshow('S7', S)
        # cv2.waitKey(0)

        # cv2.imshow('V8', V)
        # cv2.waitKey(0)

def save_hsv(src_dir,dst_dir):
    if not os.path.exists(dst_dir + '/h'):
        os.makedirs(dst_dir + '/h')
    if not os.path.exists(dst_dir + '/s'):
        os.makedirs(dst_dir + '/s')
    if not os.path.exists(dst_dir + '/v'):
        os.makedirs(dst_dir + '/v')
    if not os.path.exists(dst_dir + '/hsv'):
        os.makedirs(dst_dir + '/hsv')
    for one_img in os.listdir(src_dir):
        one_img_path = src_dir + '/' + one_img
        defect = str(one_img.split('.')[0]) + '.png'
        origin = str(one_img.split('.')[0]) + '_0.png'

        h_path1 = dst_dir + '/h/' + defect
        h_path2 = dst_dir + '/h/' + origin

        s_path1 = dst_dir + '/s/' + defect
        s_path2 = dst_dir + '/s/' + origin

        v_path1 = dst_dir + '/v/' + defect
        v_path2 = dst_dir + '/v/' + origin

        hsv_path1 = dst_dir + '/hsv/' + defect
        hsv_path2 = dst_dir + '/hsv/' + origin

        img = Image()
        img.from_file(one_img_path)
        defect_img = image2numpy(img.visual_at(0))
        hsv = cv2.cvtColor(defect_img, cv2.COLOR_BGR2HSV)
        H,S,V = cv2.split(hsv)

        cv2.imwrite(h_path1,H)
        cv2.imwrite(s_path1,S)
        cv2.imwrite(v_path1,V)
        cv2.imwrite(hsv_path1,hsv)

        origin_img = image2numpy(img.visual_at(1))
        hsv = cv2.cvtColor(origin_img, cv2.COLOR_BGR2HSV)
        H,S,V = cv2.split(hsv)

        cv2.imwrite(h_path2,H)
        cv2.imwrite(s_path2,S)
        cv2.imwrite(v_path2,V)
        cv2.imwrite(hsv_path2,hsv)

    


def trans2hsv(src_dir,dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for one_img in os.listdir(src_dir):
        src_path = src_dir + '/' + one_img
        dst_path = dst_dir + '/' + one_img
        trans_one(src_path,dst_path)

def trans_one(src_path,dst_path):
    img = Image()
    img.from_file(src_path)
    defect_img = image2numpy(img.visual_at(0))
    origin_img = image2numpy(img.visual_at(1))
    defect_hsv = cv2.cvtColor(defect_img, cv2.COLOR_BGR2HSV)
    origin_hsv = cv2.cvtColor(origin_img, cv2.COLOR_BGR2HSV)

    batch_img = BatchImage([numpy2image(defect_hsv),numpy2image(origin_hsv), img.visual_at(2)])
    img_out = Image()
    img_out.from_batch(batch_img)
    img_out.to_file(dst_path)


if __name__ == '__main__':

    # src_dir = r'D:\yang.xie\aidi_projects\20201222-rgbhs\cls_roi_b\Classify_0\source'
    # dst_dir = r'D:\yang.xie\aidi_projects\20201222-rgbhs\generate_label\Detection_0\source_hsv'

    # trans2hsv(src_dir,dst_dir)

    show_list = [110, 115, 1973, 1973, 1973, 1973, 1976, 2019, 2019, 2019, 2019, 2019, 2338, 2345, 2345, 2345, 2345, 2345, 2345, 2345, 2345, 3326, 3326, 3326, 3326, 3326, 3547, 3547, 3547, 3547, 3547, 3547, 3547, 4130, 4130, 4130, 4130, 4130, 4130, 4130, 4142, 4435, 4435, 4435, 4435, 4435, 4435, 4435, 4435, 5265, 5265, 5265, 6844, 6844, 7457, 7457, 7457, 8685, 8685, 8685, 8950, 8982, 9003, 9255, 9255, 9255, 9305, 9305, 9385, 9385, 9855, 9855, 9855, 9855, 9855, 9855]
    # show_list = [2345,4435,1973,2019,3547,4130,6844,8982,9305,9855]

    root_dir = r'D:\yang.xie\aidi_projects\20201222-rgbhs\cls_roi_r\Classify_0\source'
    for one_index in show_list:    
        src_path = root_dir + '/' + str(one_index) + '.aqimg'
        show(src_path,one_index)

    # src_path = r'D:\yang.xie\aidi_projects\20201222-rgbhs\cls_roi_r\Classify_0\source'
    # dst_path = r'D:\yang.xie\aidi_projects\20201222-rgbhs\cls_roi_r\Classify_0\hsv'
    # save_hsv(src_path,dst_path)








