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
        ok_img = image2numpy(img.visual_at(1))
        # hsv = cv2.cvtColor(defect_img, cv2.COLOR_BGR2HSV)
        # H,S,V = cv2.split(hsv)
        # R,G,B = cv2.split(defect_img)
        defect_img = defect_img.astype(np.int8)
        ok_img = ok_img.astype(np.int8)

        # img = ok_img - defect_img
        img = defect_img - ok_img

        print(img[0][0])
        # img = abs(img)

        img = img.astype(np.uint8)
        defect_img = defect_img.astype(np.uint8)
        ok_img = ok_img.astype(np.uint8)

        root_dir = r'D:\yang.xie\aidi_projects\20201117-iteration4\iter04\RegClassify_0\source\1714.aqimg'

        img2 = Image()

        img2.from_file(root_dir)
        defect_img2 = image2numpy(img2.visual_at(0))
        img_add = defect_img2 + img
        img_add = img_add.astype(np.uint8)



        print(defect_img[0][0])
        print(ok_img[0][0])
        print(img[0][0])

        cv2.imshow('HSV1', img_add)
        cv2.waitKey(0)

        
        cv2.imshow('HSV1', img)
        cv2.waitKey(0)

        cv2.imshow('HSV1', defect_img)
        cv2.waitKey(0)

        cv2.imshow('HSV1', ok_img)
        cv2.waitKey(0)


if __name__ == '__main__':
    root_dir = r'D:\yang.xie\aidi_projects\20201117-iteration4\iter04\RegClassify_0\source'
    # 388 8689 6827 8715 4064
    one_index = 9229
    src_path = root_dir + '/' + str(one_index) + '.aqimg'
    show(src_path,one_index)









