
import os
import sys
import cv2
import random
import re

def _get_indexs(path):
    res = []
    for files in os.listdir(path):
        dd, ff = os.path.split(files)
        fname, ext = os.path.splitext(ff)
        res.append(fname.strip())

    return res



def _write_indexs(path, indexs):
    with open(path, "w", encoding="utf-8") as f:
        for i in indexs:
            f.write(str(i) + "\n")

def _write_indexs_in_list_format(path, indexs):
    with open(path, "w", encoding="utf-8") as f:
        f.write("[")
        for i in indexs:
            f.write(str(i)+",")
        f.write("]")

def sort_key(s):
    if s:
        try:
            c = re.findall("^\d+", s)[0]
        except:
            c = -1
        return int(c)

def script_gen_indexs():
    root_dir = "D:/yang.xie/aidi_projects/update-label0918"
    src_dir = root_dir + "/tmp_single_set/source"

    # file_path = root_dir + "/train_indexs.txt"
    file_path = root_dir + "/tmp_single_set.txt"

    indexs = _get_indexs(src_dir)
    indexs.sort(key = sort_key )
    print("indexs len: ", len(indexs))

    random.shuffle(indexs)
    _write_indexs_in_list_format(file_path, indexs)



if __name__=="__main__":
    script_gen_indexs()
