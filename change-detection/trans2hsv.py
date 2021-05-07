import os
import sys
import cv2
import json
import shutil
import numpy as np

sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *


def kernel(img,i,j,s):
    sum = 0.
    for row in range(i-s,i+s+1):
        for col in range(j-s,j+s+1):
            sum = sum + img[row][col]
    #         print('for sum: ',sum)
    #         print('pix: ',img[row][col])
    # print('sum:  ',sum)
    res = sum/((2*s+1)*(2*s+1))
    # print('res:  ',res)
    return res


def img_filter(img):
    h = img.shape[0]
    w = img.shape[1]
    for i in range(1,h-1):
        for j in range(1,w-1):
            img[i][j] = int(kernel(img,i,j,1))
    return img

show_list = [1732,388,1740,1741,8715,2345,3326,1976,1026,3547,4435]

def contrast_enhance(img):

    cv2.imshow('origin_img', img)
    cv2.waitKey(0)
    h = img.shape[0]
    w = img.shape[1]
    total = h*w

    for i in range(5):
        img = img_filter(img)

    pix_dict = {}
    # pix_list = []
    for i in range(256):
        pix_dict[i] = 0
        # pix_list.append(0)

    for i in range(h):
        for j in range(w):
            pix_dict[img[i][j]] = pix_dict[img[i][j]] + 1

    tmp_dict = sorted(pix_dict.items(), key = lambda kv:(kv[1], kv[0]))
    print(tmp_dict)

    top_list = []
    for i in range(2):
        top_list.append(tmp_dict[255-i][0])
    print(top_list)

    en_list = []
    for one_index in top_list:
        en_list.append(one_index - 3)
        en_list.append(one_index - 2)
        en_list.append(one_index - 1)
        en_list.append(one_index)
        en_list.append(one_index+1)
        en_list.append(one_index+2)
        en_list.append(one_index+3)

    print(en_list)

    # for i in range(256):
    #     pix_dict[i] = 0
    # for i in range(h):
    #     for j in range(w):
    #         pix_dict[img1[i][j]] = pix_dict[img1[i][j]] + 1
    # print(pix_dict)

    # for i in range(256):
    #     if i == 0:
    #         pix_list[i] = pix_dict[i]/total
    #     else:
    #         pix_list[i] = pix_list[i-1] + pix_dict[i]/total

    # print(pix_list)

    # cv2.imshow('origin_img', img1)
    # cv2.waitKey(0)

    # for i in range(h):
    #     for j in range(w):
    #         img[i][j] = img[i][j] + (img[i][j] - img1[i][j])*(img[i][j] - img1[i][j])

    # for i in range(h):
    #     for j in range(w):
    #         img[i][j] = pix_list[img[i][j]]*255 + 0.5

    # for i in range(h):
    #     for j in range(w):
    #         float_num = float(img[i][j])
    #         tmp = float_num*float_num
    #         tmp = tmp/10
    #         if tmp > 255:
    #             tmp = 255
    #         img[i][j] = int(tmp)

    # for i in range(h):
    #     for j in range(w):
    #         if img[i][j] >28 and img[i][j] < 45:
    #             img[i][j] += 40

    for i in range(h):
        for j in range(w):
            if img[i][j] in en_list:
                img[i][j] += 40

    cv2.imshow('origin_img', img)
    cv2.waitKey(0)

def show(src_path,one_index):
        img = Image()
        img.from_file(src_path)

        defect_img = image2numpy(img.visual_at(0))
        defect_img = defect_img.astype(np.uint8)
        R,G,B = cv2.split(defect_img)

        normal_img = image2numpy(img.visual_at(1))
        normal_img = normal_img.astype(np.uint8)
        R1,G1,B1 = cv2.split(normal_img)

        contrast_enhance(R1)

        # hsv = cv2.cvtColor(defect_img, cv2.COLOR_BGR2YCrCb)
        hsv = cv2.cvtColor(defect_img, cv2.COLOR_BGR2HSV)

        H,S,V = cv2.split(hsv)

        contrast_enhance(R)

        
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

    # show_list = [110, 115, 1973, 1976, 2019, 2338, 2345, 3326, 3547, 4130, 4142, 4435, 5265, 6844, 7457, 8685, 8950, 8982, 9003, 9255, 9305, 9385, 9855, 20000,20001,20002,20003,20004]
    # show_list = [2345,4435,1973,2019,3547,4130,6844,8982,9305,9855]

    root_dir = r'D:\yang.xie\aidi_projects\20201222-rgbhs\cls_roi_r\Classify_0\source'
    for one_index in show_list:    
        src_path = root_dir + '/' + str(one_index) + '.aqimg'
        show(src_path,one_index)

    # src_path = r'D:\yang.xie\aidi_projects\20201222-rgbhs\cls_roi_r\Classify_0\source'
    # dst_path = r'D:\yang.xie\aidi_projects\20201222-rgbhs\cls_roi_r\Classify_0\hsv'
    # save_hsv(src_path,dst_path)








