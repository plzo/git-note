

import os
import sys

from aidi410.aidi_vision import *


def batch_json2aqlabel():
    root_dir = "D:/yang.xie/aidi_projects/check_class/xbq-b/RegClassify_0"
    json_dir = root_dir + "/label"
    img_dir = root_dir + "/source_aqimg"
    dst_dir = root_dir + "/label_aqlabel"
    if not os.path.exists(json_dir):
	    os.makedirs(json_dir)
    
    indexs = _get_indexs(img_dir)
    count = 0
    for ii in indexs:
        print("ii ", ii)
        img_path = img_dir + "/" + ii + ".aqimg"
        json_path = json_dir + "/" + ii + ".json"
        aqlabel_path = dst_dir + "/" + ii + ".aqlabel"
        
        i_label = LabelIO()
        read_33X_classify_label(json_path, img_path, i_label)
        i_label.save_to(aqlabel_path)
        count +=1

        # if count==2:
        #     break




def _get_indexs(path):
    res = []
    for files in os.listdir(path):
        if os.path.isfile(path + "/" + files):
            dd, ff = os.path.split(files)
            fname, ext = os.path.splitext(ff)
            res.append(fname.strip())

    return res







if __name__=="__main__":
    batch_json2aqlabel()

