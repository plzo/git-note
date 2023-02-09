
import os
import sys
import cv2

from aidi410.aidi_vision import *


# transform 6c_1img xml to 3c_2img aqimg
def batch_xml2aqimg():
    root_dir = "D:/yang.xie/aidi_projects/check_class/xbq-b/RegClassify_0/"
    src_dir = root_dir + "source"
    dst_dir = root_dir + "source_aqimg"
    isExists=os.path.exists(dst_dir)
    if not isExists:
        os.makedirs(dst_dir) 
    group_num = 2
    base_c = 3
    indexs = _get_indexs(src_dir)
    
    for idx in indexs:
        src_file = src_dir + "/" + str(idx) + ".xml"
        dst_file = dst_dir + "/" + str(idx) + ".aqimg"

        img = Image()
        img.from_xml_file(src_file)
        img.group(group_num, base_c)
        img.to_file(dst_file)

    return True
    

def _get_indexs(path):
    res = []
    for files in os.listdir(path):
        dd, ff = os.path.split(files)
        fname, ext = os.path.splitext(ff)
        res.append(fname.strip())

    return res



def test_xml2aqimg():
    root_dir = "D:/siqin/debug_dir/xml_debug"
    src_file = root_dir + "/src/1.xml"

    dst_dir = root_dir + "/dst"
    dst_file = dst_dir + "/1.aqimg"
    print("hi")

    # read xml file
    img = Image()
    img.from_xml_file(src_file)

    total_c = img.channels()
    num = img.visual_size()
    print("total_c: {0}, num: {1}".format(total_c, num))
    
    img.group(2, 3)

    total_c = img.channels()
    num = img.visual_size()
    print("total_c: {0}, num: {1}".format(total_c, num))
    
    one = img.visual_at(0)
    two = img.visual_at(1)
    # one.show()
    # two.show()

    one.to_file(dst_dir + "/one.bmp")
    two.to_file(dst_dir + "/two.bmp")

    img.to_file(dst_file)

    # load new aqimg file
    img2 = Image()
    img2.from_file(dst_file)
    total_c = img.channels()
    num = img.visual_size()
    print("total_c: {0}, num: {1}".format(total_c, num))





    


if __name__=="__main__":
    # test_xml2aqimg()

    batch_xml2aqimg()



