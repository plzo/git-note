import os
import sys

# inputdir = 'D:/yang.xie/aidi_projects/project-20201022/classify_no_reg/Classify_0/label'
# inputdir = 'D:/yang.xie/aidi_projects/cls-seg20201027/data/processed/label_seg'


inputdir = 'D:/yang.xie/aidi_projects/shennan1107/label_combine_2/fengehuigui/Segment_0/label'

# inputdir = 'D:/yang.xie/aidi_projects/shennan1107/label_combine_2/huiguifenge/RegClassify_0/label'



output = inputdir + '/../seg_label_list.txt'

def makelist():
    fp=open(output,'w')    
    for one_file in os.listdir(inputdir):
        if one_file.endswith('.aqlabel'):                       
            fp.write(inputdir + '/' + one_file)
            fp.write('\n')      
makelist()
