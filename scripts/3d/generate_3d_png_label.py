import os
import sys
import cv2
import json
import numpy as np
import tifffile as tiff
import shutil
import random

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
            points.append([[one_point['x'],one_point['y']]])
        points_set.append(points)
    return points_set

count = 1

def crop_img(input_path,out_path,name,mat,crop,w,h,rand_on,x,y):
    img_h = mat.shape[0]
    img_w = mat.shape[1]

    img_png = cv2.imread(input_path + '/' + name + '.bmp')
    img_tiff = tiff.imread(input_path + '/' + name + '.tif')

    if rand_on:
        crop_x = int(random.random() * (img_w - w))
        crop_y = int(random.random() * (img_h - h))
    else:
        crop_x = x
        crop_y = y
        if crop_x + w > img_w:
            crop_x = img_w - w
        if crop_y + h > img_h:
            crop_y = img_h- h        
    if crop:
        mat = mat[int(crop_y):int(crop_y + h),int(crop_x):int(crop_x + w)]
        img_png = img_png[int(crop_y):int(crop_y + h),int(crop_x):int(crop_x + w)]
        img_tiff = img_tiff[int(crop_y):int(crop_y + h),int(crop_x):int(crop_x + w)]

    # print('mat.shape: ',mat.shape)

    cv2.imwrite(out_path + '/gt/' + name + '.png', mat)
    cv2.imwrite(out_path + '/rgb/' + name + '.bmp', img_png)
    tiff.imsave(out_path + '/xyz/' + name + '.tif', img_tiff)


def process_one_dir(input_path,out_path):
    if not os.path.exists(out_path + '/rgb/'):
        os.makedirs(out_path + '/rgb/')
    if not os.path.exists(out_path + '/gt/'):
        os.makedirs(out_path + '/gt/')
    if not os.path.exists(out_path + '/xyz/'):
        os.makedirs(out_path + '/xyz/')

    crop = False
    crop_w = 128
    crop_h = 128
    for one_file in os.listdir(input_path):
        if one_file.endswith('.tif'):
            name = one_file.split('.tif')[0]
            print(input_path + '/' + one_file)
            label_name = name + '.aqlabel'
            tiff_data = tiff.imread(input_path + '/' + one_file)
            mat = np.zeros(tiff_data.shape,dtype=np.uint8)

            if os.path.exists(input_path + '/' + label_name):

                points_set = get_points_set(input_path + '/' + label_name)
                if len(points_set) == 0:
                     crop_img(input_path,out_path,name,mat,crop,crop_w,crop_h,True,0,0)

                # for one_set in points_set:
                #     new_set = []
                #     new_set.append(one_set)
                #     contours = np.array(new_set).astype(np.int32)
                #     cv2.drawContours(mat,contours,-1,255,-1)

                # for one_set in points_set:
                #     x,y,w,h = cv2.boundingRect(np.array(one_set).astype(np.int32))
                #     x = max(x + w/2 - crop_w/2,0)
                #     y = max(y + h/2 - crop_h/2,0)
                #     crop_img(input_path,out_path,name,mat,crop,crop_w,crop_h,False,x,y)
            else:
                crop_img(input_path,out_path,name,mat,crop,crop_w,crop_h,True,0,0)

def process_all(root_dir,out_dir):
    for one_dir in os.listdir(root_dir):
        print(one_dir)
        # if one_dir == 'baodian' or one_dir == 'good':
        #     continue
        if os.path.isdir(root_dir + '/' + one_dir):
            out_path = out_dir + '/' + one_dir
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            process_one_dir(root_dir + '/' + one_dir, out_path)
            print('----------complete-----------:  ',one_dir)


if __name__ == '__main__':
    root_dir = r'F:\yang.xie\data\20220301_3D\0414_Dinghan\2.3 tiff_bmp_aqlabel'
    out_dir = r'F:\yang.xie\data\20220301_3D\0414_Dinghan\3.4 png_label_nocrop_ok\type1\test'
    # out_dir = r'F:\yang.xie\workspace\data\dinghan20220426_aqlabel_with_num'

    process_all(root_dir,out_dir)




