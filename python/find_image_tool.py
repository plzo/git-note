import os
import sys
import cv2
import json
import shutil


def clear_dir(dir_path):
    for one_file in os.listdir(dir_path):
        one_file_path = dir_path + '/' + one_file
        os.remove(one_file_path)
    print('delete file * :', dir_path)



def find_index(image_dir):
    index_dict = {}
    index_list = []
    for one_test_dir in os.listdir(image_dir):
        if os.path.isdir(image_dir + '/' + one_test_dir):
            for one_img in os.listdir(image_dir + '/' + one_test_dir):
                if one_img.endswith('.png'):
                    strs = one_img.strip().split('.png')[0].split('#')
                    cls_ans = strs[1].split('~')[0]
                    roi_cls_ans = strs[2].split('~')[0]
                    enhance_cls_ans = strs[3].split('~')[0]
                    final_ans = strs[4].split('~')[0]

                    gt_label = strs[5]
                    gt_cb_label = strs[6]
                    gt_lv_label = strs[7]

                    flag = cls_ans != gt_cb_label or roi_cls_ans != gt_cb_label or enhance_cls_ans != gt_cb_label

                    if flag:
                        index_dict[strs[0]] = 1

    for key in index_dict.keys():
        index_list.append(int(key))
    
    print(index_list)
    print(len(index_list))




def copy_data(src_dir,dst_dir,rf_dir):
    for one_img in os.listdir(rf_dir):
        index = one_img.strip().split('.png')[0].split('#')[0]
        for one_src_img in os.listdir(src_dir):
            if one_src_img.strip().split('.png')[0].split('#')[0] == index:
                shutil.copy(src_dir + '/' + one_src_img, dst_dir + '/' + one_src_img)
                break


def judge(dict1,dict2):
    gt_cb_label = dict1['strs'][-1]
    flag = dict2['strs'][2] == 'OK' and gt_cb_label != 'OK' and dict1['strs'][2] != 'OK'

    return flag

def find_image2(src_dir1,src_dir2):
    dst_dir = src_dir2 + '/cross'
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    clear_dir(dst_dir)
    dict1 = {}
    for one_img in os.listdir(src_dir1):
        if one_img.endswith('.png'):
            strs = one_img.strip().split('.png')[0].split('#')
            dict0 = {}
            dict0['index'] = strs[0]
            dict0['strs'] = strs
            dict0['one_img'] = one_img
            dict0['path'] = src_dir1 + '/' + one_img
            dict1[strs[0]] = dict0
    dict2 = {}
    for one_img in os.listdir(src_dir2):
        if one_img.endswith('.png'):
            strs = one_img.strip().split('.png')[0].split('#')
            dict0 = {}
            dict0['index'] = strs[0]
            dict0['strs'] = strs
            dict0['one_img'] = one_img
            dict0['path'] = src_dir2 + '/' + one_img
            # print(dict0['path'])

            dict2[strs[0]] = dict0

    index_list = []

    for k in dict1:
        if judge(dict1[k],dict2[k]):
            # print(dst_dir + '/' + one_img.replace('.png','_1.png'))
            # shutil.copy(dict2[k]['path'], dst_dir + '/' + one_img.replace('.png','_2.png'))
            shutil.copy(dict1[k]['path'], dst_dir + '/' + dict1[k]['one_img'].split('.png')[0] + '_1.png')
            shutil.copy(dict2[k]['path'], dst_dir + '/' + dict2[k]['one_img'].split('.png')[0] + '_2.png')
            index_list.append(int(dict1[k]['index']))

    print(index_list)


def compare_AB(A,B):
    dst_dir = A + '_cp'
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    clear_dir(dst_dir)
    A_ids = []
    B_ids = []
    dst_ids = []
    ids = []
    for one_img in os.listdir(A):
        if one_img.endswith('.png'):
            strs = one_img.strip().split('.png')[0].split('#')
            A_ids.append(strs[0])
    for one_img in os.listdir(B):
        if one_img.endswith('.png'):
            strs = one_img.strip().split('.png')[0].split('#')
            B_ids.append(strs[0])
    for one_id in A_ids:
        if one_id not in B_ids:
            dst_ids.append(one_id)
    for one_img in os.listdir(A):
        if one_img.endswith('.png'):
            strs = one_img.strip().split('.png')[0].split('#')
            if strs[0] in dst_ids:
                shutil.copy(A + '/' + one_img, dst_dir + '/' + one_img)
                ids.append(int(strs[0]))
    print(ids)



def find_image(image_dir):
    dst_dir = image_dir + '/漏检all'
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    clear_dir(dst_dir)
    ids = []
    for one_img in os.listdir(image_dir):
        if one_img.endswith('.png'):
            strs = one_img.strip().split('.png')[0].split('#')
            cls_ans = strs[1]
            roi_cls_ans = strs[2]
            enhance_cls_ans = strs[3]
            hsv_ans = strs[4]
            combine_ans = strs[5]

            fenji_ans = strs[7]

            gt_label = strs[-3]
            gt_cb_label = strs[-2]
            gt_lv_label = strs[-1]

            # flag = strs[7] != gt_lv_label

            # flag = strs[1] != gt_cb_label and strs[2] != gt_cb_label and strs[3] == gt_cb_label and gt_cb_label != "OK" #12错3对
            # flag = (strs[1] == gt_cb_label and strs[2] == gt_cb_label) and strs[3] != gt_cb_label and gt_cb_label != "OK"

            # flag = strs[1] == "OK" and strs[2] == "OK" and strs[3] == "OK" and strs[5] != "OK"  #123漏cb不漏


            # flag = strs[5] == gt_cb_label and strs[6] != gt_label

            # flag = (cls_ans == "OK" or roi_cls_ans == "OK" or enhance_cls_ans == "OK" or strs[4] == "OK" or strs[5] == "OK") and gt_cb_label != "OK"  # 漏检

            # flag = (cls_ans == "OK" and roi_cls_ans == "OK" and enhance_cls_ans == "OK" and strs[4] == "OK" and strs[5] == "OK" and strs[7] != "OK") and gt_cb_label != "OK"  # 漏检
            # flag = (cls_ans == "OK" or roi_cls_ans == "OK" or enhance_cls_ans == "OK" or hsv_ans == "OK") and gt_cb_label != "OK"  # 漏检
            # flag = (strs[1] == "OK" or strs[2] == "OK" or strs[4] == "OK" or strs[5] == "OK" or strs[6] == "OK") and gt_cb_label != "OK"  # 漏检
            # flag = (cls_ans == "OK" and roi_cls_ans == "OK" and enhance_cls_ans == "OK" and hsv_ans == "OK") and gt_cb_label != "OK" # 漏检all

            # flag = gt_cb_label.split('-')[-1] == "严重" and (combine_ans.split('-')[-1] == "轻度" or combine_ans == "OK") #漏检
            flag = gt_lv_label.split('-')[-1] == "严重" and (fenji_ans.split('-')[-1] == "轻度" or fenji_ans == "OK") #漏检
            # flag = gt_lv_label.split('-')[-1] == "严重" and (fenji_ans == "OK") #漏检
            # flag = strs[5] != gt_lv_label and gt_lv_label.split('-')[1] == '严重'
            

            # flag = cls_ans == "OK" and gt_cb_label != "OK"  # 漏检1
            # flag = roi_cls_ans == "OK" and gt_cb_label != "OK"  # 漏检2
            # flag = enhance_cls_ans == "OK" and gt_cb_label != "OK"  # 漏检3
            # flag = strs[1] == "OK" and gt_cb_label != "OK" # 漏检4

            # flag = strs[1] == "OK" and strs[2] == "OK" and strs[3] != "OK" and gt_cb_label != "OK" #只3正确
            # flag = strs[1] == "OK" and strs[2] != "OK" and strs[3] == "OK" and gt_cb_label != "OK" #只2正确
            # flag = strs[1] != "OK" and strs[2] == "OK" and strs[3] == "OK" and gt_cb_label != "OK" #只1正确

            # flag = strs[1] == "OK" and strs[2] != "OK" and gt_cb_label != "OK" #1漏2不漏
            # flag = strs[1] == "OK" and strs[3] != "OK" and gt_cb_label != "OK" #1漏3不漏
            # flag = strs[1] == "OK" and strs[2] != "OK" and strs[3] != "OK" and gt_cb_label != "OK" #1漏23不漏


            # flag = gt_cb_label == "OK" and (enhance_cls_ans != "OK")  #过检3
            # flag = gt_cb_label == "OK" and (strs[4] != "OK")  #过检4
            # flag = gt_cb_label == "OK" and (cls_ans != "OK" or roi_cls_ans != "OK" or enhance_cls_ans != "OK" or hsv_ans != "OK")  #过检
            # flag = gt_cb_label == "OK" and (combine_ans != "OK")  #过检
            # flag = gt_cb_label == "OK" and (cls_ans == "OK" and roi_cls_ans == "OK" and enhance_cls_ans == "OK" and combine_ans != "OK")  #过检
            # flag = gt_cb_label == "OK" and (cls_ans != "OK" and roi_cls_ans != "OK" and enhance_cls_ans != "OK")  #过检all
            # flag = gt_cb_label == "OK" and (strs[1] != "OK" or strs[2] != "OK" or strs[4] != "OK" or strs[5] != "OK"  or strs[6] != "OK")  #过检
            # flag = gt_label != "IC绿油-脱落" and hsv_ans != "OK"
            # flag = gt_label == "IC绿油-脱落"

            # flag = gt_cb_label != roi_cls_ans  #混淆

            # flag = cls_ans == "OK" and gt_cb_label != "OK" and (roi_cls_ans != "OK")  #1漏2不漏
            # flag = roi_cls_ans == "OK" and gt_cb_label != "OK" and (cls_ans != "OK")  #2漏1不漏
            # flag = roi_cls_ans == "OK" and gt_cb_label != "OK" and (enhance_cls_ans != "OK")  #2漏3不漏
            # flag = enhance_cls_ans == "OK" and gt_cb_label != "OK" and (roi_cls_ans != "OK")  #3漏2不漏
            # flag = gt_cb_label == "OK"  #绿油-发白
            # flag = cls_ans != gt_cb_label  #错误1
            # flag = cls_ans != gt_cb_label or roi_cls_ans != gt_cb_label or enhance_cls_ans != gt_cb_label  #错误
            # flag = strs[5] != gt_cb_label

            # flag = hsv_ans == "Other" and gt_cb_label == "绿油-脱落"  #掉桥漏检
            # flag = gt_cb_label == "焊盘-曝虚"

            # flag = enhance_cls_ans != gt_cb_label and roi_cls_ans == gt_cb_label  #3ng2ok
            # flag = enhance_cls_ans == gt_cb_label and roi_cls_ans != gt_cb_label  #2ng3ok

            if flag:
                shutil.copy(image_dir + '/' + one_img, dst_dir + '/' + one_img)
                ids.append(int(strs[0]))
    print(ids)

def get_score(name):
    grade = name.split('-')[-1]
    if grade == '轻度':
        return 0.3
    elif grade == '中度':
        return 0.6
    elif grade == '严重':
        return 0.9
    else:
        print('error!')
        return -1




def find_image_grade(image_dir):
    dst_dir = image_dir + '/漏检'
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    clear_dir(dst_dir)
    ids = []
    for one_img in os.listdir(image_dir):
        if one_img.endswith('.png'):
            strs = one_img.strip().split('.png')[0].split('#')
            lv_ans = strs[3]
            gt_label = strs[4]
            gt_lv_label = strs[6]
          
            flag = get_score(lv_ans) < get_score(gt_lv_label) #漏检

            # if(flag):
            #     print(get_score(lv_ans),'lv_ans')
            #     print(get_score(gt_lv_label),'gt_lv_label')


            if flag:
                shutil.copy(image_dir + '/' + one_img, dst_dir + '/' + one_img)
                ids.append(int(strs[0]))
    print(ids)   


if __name__ == '__main__':

    # image_dir = r"F:\yang.xie\projects\20220217_chaosheng_xiufu\new_method\debug_results\baseline0224"
    # find_image(image_dir)

    path_a = r"F:\yang.xie\projects\20220217_chaosheng_xiufu\new_method\debug_results\baseline0224\漏检all"
    path_b = r"F:\yang.xie\projects\20220217_chaosheng_xiufu\old_method\debug_results\baseline0224_旧算法直接分类分级\漏检all"
    compare_AB(path_b,path_a)

    # find_image_grade(image_dir)

    # src_dir1 = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\pcb_origin_iter04\RegClassify_0\debug_results\standard'
    # src_dir2 = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\pcb_origin_iter04\RegClassify_0\debug_results\20210814bs'
    # find_image2(src_dir1,src_dir2)


    # find_index(r"D:\yang.xie\aidi_projects\20210129-pcb-newlabel\20210605_big_set_enhance\debug_results")

    # src_dir = r"D:\yang.xie\aidi_projects\20210129-pcb-newlabel\20210605_big_set_enhance\debug_results\enhance_roi_cls_16_0_15_v1-32-64-128-type1-3"
    # dst_dir = r"D:\yang.xie\aidi_projects\20210129-pcb-newlabel\20210605_big_set_enhance\debug_results\enhance_roi_cls_16_0_15_v1-32-64-128\漏检"

    # src_dir = r"D:\yang.xie\aidi_projects\20210129-pcb-newlabel\20210605_big_set_enhance\debug_results\enhance_roi_cls_16_0_15_v1-32-64-128"
    # dst_dir = r"D:\yang.xie\aidi_projects\20210129-pcb-newlabel\20210605_big_set_enhance\debug_results\enhance_roi_cls_16_0_15_v1-32-64-128-type1-3\漏检"

    # rf_dir = dst_dir
    # copy_data(src_dir,dst_dir,rf_dir)










