import os
import sys
import json
import numpy as np
import tifffile as tiff
import cv2
import shutil
import random


origin_tiff = './origin.tiff'
origin_png = './origin.png'
# origin_pts = './origin.pts'
origin_pts = './origin2.pts'
origin_pcd = './origin.pcd'
origin_label = './origin_label.png'


save_tiff = './out.tiff'
save_png = './out.png'
save_pts = './out.pts'
save_label_pts = './out_label.pts'
save_pcd = './out.pcd'

dinghan_tif = './dinghan2.tif'


def show_info(data):
    print(data.shape)  # (9, 20)
    print(type(data))  # <class 'numpy.ndarray'>
    print(type(data[0][0]))  # <class 'numpy.uint16'>
    print(data[0][0])


def test():
    img_png = cv2.imread(origin_png)
    img_tiff = tiff.imread(origin_tiff)
    img_dinghan_tif = tiff.imread(dinghan_tif)

    cv2.imshow('s',img_png)
    cv2.waitKey(0)

    print('img_png info:')
    show_info(img_png)

    print('img_tiff info:')
    show_info(img_tiff)

    print('img_dinghan_tif info:')
    show_info(img_dinghan_tif)

    tiff.imsave(save_tiff, img_png)


def pts2pcd(input_path, output_path):
    
    #Lodaing txt
    Full_Data = np.loadtxt(input_path)
    print('pts2pcd loadtxt:')
    show_info(Full_Data)
    
    #Creating pcd
    if os.path.exists(output_path):
        os.remove(output_path)
    Output_Data = open(output_path, 'a')

    Output_Data.write("# .PCD v0.7 - Point Cloud Data file format\n")
    Output_Data.write("VERSION 0.7\n")
    Output_Data.write("FIELDS x y z\n")
    Output_Data.write("SIZE 4 4 4\n")
    Output_Data.write("TYPE F F F\n")
    Output_Data.write("COUNT 1 1 1\n")
    Output_Data.write("WIDTH " + str(Full_Data.shape[0]) + "\n")
    Output_Data.write("HEIGHT 1\n")
    Output_Data.write("VIEWPOINT 0 0 0 1 0 0 0\n")
    Output_Data.write("POINTS " + str(Full_Data.shape[0]) + "\n")
    Output_Data.write("DATA ascii\n")
    for j in range(Full_Data.shape[0]):
        Output_Data.write(str(Full_Data[j,0]) + " " + str(Full_Data[j,1]) + " " + str(Full_Data[j,2]) + "\n")
    Output_Data.close()
    
    print('--------------pts2pcd Completed--------------')

def pts2pts(input_path, output_path):
    #Lodaing txt
    Full_Data = np.loadtxt(input_path)
    print('pts2pts loadtxt:')
    show_info(Full_Data)
    np.savetxt(output_path, Full_Data, delimiter=' ', fmt='%.5f')


    print('--------------Completed--------------')

global_scale = 1

def down_sample(data,scale):
    w = data.shape[0]
    h = data.shape[1]
    new_w = int(w/scale)
    new_h = int(h/scale)

    if len(data.shape) < 3:
        new_data = np.zeros((new_w,new_h))
    else:
        new_data = np.zeros((new_w,new_h,3))
    
    for c in range(new_w):
        for r in range(new_h):
            new_data[c][r] = data[int(c*scale)][int(r*scale)]

    return new_data

def label2pts(input_path,label,output_path):
    img = cv2.imread(input_path)
    img = img[:,:,0]
    w = img.shape[0]
    h = img.shape[1]
    new_w = int(w/global_scale)
    new_h = int(h/global_scale)
    new_data = np.zeros((new_w,new_h))
    
    for c in range(new_w):
        for r in range(new_h):
            if img[int(c*global_scale)][int(r*global_scale)] > 0:
                new_data[c][r] = label
            else:
                new_data[c][r] = 0
    new_data.shape = (new_w*new_h,-1)
    np.savetxt(output_path, new_data, delimiter=' ', fmt='%.5f')


def tiff2pts(input_path, output_path):
    tiff_data = tiff.imread(input_path)
    # tiff_data = np.array([(1,2,3),(4,5,6)])
    tiff_data = down_sample(tiff_data,global_scale)
    print('tiff2pts tiff.imread:')
    show_info(tiff_data)
    w = tiff_data.shape[0]
    h = tiff_data.shape[1]

    if len(tiff_data.shape) == 2:
        new_data = np.zeros((w, h, 3))
        num_count = 0
        sum_count = 0
        for c in range(w):
            for r in range(h):
                if tiff_data[c][r] > 0:
                    sum_count += tiff_data[c][r]
                    num_count += 1
        ave_z = sum_count / num_count
        for c in range(w):
            for r in range(h):
                if tiff_data[c][r] > 0:
                    new_data[c][r][1] = (c-(w/2)) * global_scale * 45
                    new_data[c][r][0] = (r-(h/2)) * global_scale * 12.5
                    new_data[c][r][2] = (tiff_data[c][r] - ave_z)
        new_data.shape = (w*h,-1)
        np.savetxt(output_path, new_data, delimiter=' ', fmt='%.5f')
    else:
        tiff_data.shape = (w*h,-1)
        np.savetxt(output_path, tiff_data, delimiter=' ', fmt='%.5f')

    print('--------------tiff2pts Completed--------------')

def process_mvtec_dataset(root_path,out_path):
    count_class = 0
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    for one_dir in os.listdir(root_path):
        one_class_path = root_path + '/' + one_dir + '/test'
        if os.path.isdir(one_class_path):
            for one_defect_dir in os.listdir(one_class_path):
                one_defect_path = one_class_path + '/' + one_defect_dir
                gt_dir = one_defect_path + '/gt'
                rgb_dir = one_defect_path + '/rgb'
                xyz_dir = one_defect_path + '/xyz'
                for one_file in os.listdir(gt_dir):
                    name = one_file.split('.')[0]
                    if count_class < 10:
                        out_name = '0' + str(count_class) + name
                    else:
                        out_name = str(count_class) + name
                    gt_path = gt_dir + '/' + name + '.png'
                    rgb_path = rgb_dir + '/' + name + '.png'
                    xyz_path = xyz_dir + '/' + name + '.tiff'

                    out_label_pts = out_path + '/' + out_name + '.seg'
                    out_img_pts = out_path + '/' + out_name + '.pts'
                    out_pcd = out_path + '/' + out_name + '.pcd'

                    out_gt = out_path + '/' + out_name + '_label.png'
                    out_rgb = out_path + '/' + out_name + '.png'
                    out_xyz = out_path + '/' + out_name + '.tiff'

                    shutil.copy(gt_path, out_gt)
                    shutil.copy(rgb_path, out_rgb)
                    shutil.copy(xyz_path, out_xyz)

                    # label = count_class
                    label = 1
                    print(gt_path)
                    label2pts(gt_path,label,out_label_pts)
                    tiff2pts(xyz_path, out_img_pts)
                    pts2pcd(out_img_pts, out_pcd)
                print('缺陷类别：',one_defect_dir,' label：',count_class)
                count_class += 1
            print('物体类别：',one_class_path)
    print('--------------process_mvtec_dataset Completed--------------')
    
            
def split_dataset(input_path,out_path):
    name_list = []
    for one_file in os.listdir(input_path):
        if one_file.endswith('.seg'):
            name = one_file.split('.')[0]
            name_list.append(name)
    
    total_num = len(name_list)
    val_num = int(total_num * 0.1)
    test_num = int(total_num * 0.2)
    train_num = total_num - val_num - test_num

    val_list = []
    test_list = []
    train_list = []

    for i in range(val_num):
        num = int(random.random() * len(name_list))
        val_list.append(name_list[num])
        name_list.pop(num)

    for i in range(test_num):
        num = int(random.random() * len(name_list))
        test_list.append(name_list[num])
        name_list.pop(num)

    train_list = name_list

    if not os.path.exists(out_path + '/train_val/001'):
        os.makedirs(out_path + '/train_val/001')
    for one_name in train_list:
        shutil.copy(input_path + '/' + one_name + '.seg', out_path + '/train_val/001/' + one_name + '.seg')
        shutil.copy(input_path + '/' + one_name + '.pts', out_path + '/train_val/001/' + one_name + '.pts.train')

    for one_name in val_list:
        shutil.copy(input_path + '/' + one_name + '.seg', out_path + '/train_val/001/' + one_name + '.seg')
        shutil.copy(input_path + '/' + one_name + '.pts', out_path + '/train_val/001/' + one_name + '.pts.val')

    if not os.path.exists(out_path + '/test/001'):
        os.makedirs(out_path + '/test/001')

    for one_name in test_list:
        shutil.copy(input_path + '/' + one_name + '.seg', out_path + '/test/001/' + one_name + '.seg')
        shutil.copy(input_path + '/' + one_name + '.pts', out_path + '/test/001/' + one_name + '.pts')



if __name__ == '__main__':
    # test()
    # pts2pcd(origin_pts, save_pcd)

    # tiff2pts(dinghan_tif,save_pts)
    # pts2pcd(save_pts,save_pcd)

    # label2pts(origin_label,1,save_label_pts)
    # tiff2pts(origin_tiff, save_pts)
    # pts2pcd(save_pts, save_pcd)

    # mvtec_path = r'F:\yang.xie\projects\3D\mvt_dataset'
    # mvtec_out_path = r'F:\yang.xie\workspace\SparseConvNet\examples\mvtec'

    # process_mvtec_dataset(mvtec_path,mvtec_out_path)

    test_input = r'F:\yang.xie\workspace\SparseConvNet\examples\tmp'
    test_output = r'F:\yang.xie\workspace\SparseConvNet\examples\mvtec_anormal'
    split_dataset(test_input,test_output)



