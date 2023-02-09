import os
import sys

root_dir = r'D:\yang.xie\aidi_projects\20210129-pcb-newlabel\channel_display\Classify_0'
label_dir = root_dir + '/label'
image_dir = root_dir + '/source'
output_label = label_dir + '/../label_list.txt'
output_image = image_dir + '/../image_list.txt'

def makelist_label():
    fp=open(output_label,'w')    
    for one_file in os.listdir(label_dir):
        if one_file.endswith('.aqlabel'):                       
            fp.write(label_dir + '/' + one_file)
            fp.write('\n')      


def makelist_image():
    fp=open(output_image,'w')    
    for one_file in os.listdir(image_dir):
        if one_file.endswith('.aqimg'):                       
            fp.write(image_dir + '/' + one_file)
            fp.write('\n')   


makelist_label()
makelist_image()
