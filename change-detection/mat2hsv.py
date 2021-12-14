import os
import sys
import cv2
import json
import shutil
import numpy as np

sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *



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


def trans2hsv_png(src_dir,dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for one_img in os.listdir(src_dir):
        print(one_img)
        src_path = src_dir + '/' + one_img
        dst_path = dst_dir + '/' + one_img
        trans_one_png(src_path,dst_path)

def trans_one_png(src_path,dst_path):
    img = cv2.imread(src_path)
    print(src_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    H,S,V = cv2.split(hsv)
    cv2.imwrite(dst_path,H)



if __name__ == '__main__':
    src_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\test_diaoqiao\diaoqiao1\Classify_0\source'
    dst_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\test_diaoqiao\diaoqiao1\Classify_0\hsv_source'
    trans2hsv_png(src_dir,dst_dir)  