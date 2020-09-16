import os
import sys
import random

rootdir='./'
output=rootdir+'luyan_filelist.txt'
inputdir='luyan_use/'
# inputdir='img/'
output2=rootdir+'luyan_train.txt'
data=' 0 0 0 0'
def makelist():
    fp=open(output,'w')
    fp2=open(output2,'w')
    filelist=[]
    flag=0
    for file in os.listdir(rootdir+inputdir):
        if file.endswith('png'):
            filelist.append(flag)
            wdata=inputdir+file+data
            fp.write(wdata)
            fp.write('\n')
            flag+=1
    random.shuffle(filelist)
  
    for i in filelist:

        fp2.write(str(i))
        fp2.write('\n')
      
      

makelist()
