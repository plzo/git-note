
import os,shutil
srcfile='./luyan000'
dstfile='./luyan_use000'


if not os.path.exists(dstfile):
    os.mkdir(dstfile)
for subdir in os.listdir(srcfile):
    thepath=os.path.join(srcfile,subdir)
    for file in os.listdir(thepath):
        if file.endswith('.png') or file.endswith('.json'):
            filepath=os.path.join(thepath,file)
            shutil.copy(filepath,dstfile)


