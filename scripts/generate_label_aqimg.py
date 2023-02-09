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


def png2seg_label(png_path, aqlabel_path):
    tmp_path = './tmp.png'
    out_label = LabelIO()
    tmp_img = cv2.imread(png_path)
    tmp_img = 255 - tmp_img
    cv2.imwrite(tmp_path, tmp_img)
    read_33X_segment_label(tmp_path, out_label)
    out_label.save_to(aqlabel_path)


def img2aqimg(img_path1,img_path2,aqimg_path):
    img1 = cv2.imread(img_path1)
    img2 = cv2.imread(img_path2)
    batch_img = BatchImage([numpy2image(img1),numpy2image(img2)])

    img_out = Image()
    img_out.from_batch(batch_img)
    img_out.to_file(aqimg_path)

def trans_one_dir(dir_A, dir_B, dir_label, source_dir, label_dir):
    if not os.path.exists(source_dir):
        os.makedirs(source_dir)
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)
    for one_name in os.listdir(dir_label):
        index = one_name.split('.')[0]
        img2aqimg(dir_A + '/' + one_name, dir_B + '/' + one_name, source_dir + '/' + index + '.aqimg')
        png2seg_label(dir_label + '/' + one_name, label_dir + '/' + index + '.aqlabel')

def trans_CDD(root_dir, out_dir):
    for one_dir in os.listdir(root_dir):
        if not os.path.exists(out_dir + '/' + one_dir):
            os.makedirs(out_dir + '/' + one_dir)
        trans_one_dir(root_dir + '/' + one_dir + '/A',root_dir + '/' + one_dir + '/B', \
        root_dir + '/' + one_dir + '/OUT',out_dir + '/' + one_dir + '/source', \
        out_dir + '/' + one_dir + '/label')

if __name__ == '__main__':
    trans_CDD(r'F:\yang.xie\data\20220610_CD\CDD\ChangeDetectionDataset\Real\subset',r'F:\yang.xie\data\20220610_CD\CDD\process\Real\subset')




