
import os,shutil
srcfile='luyan_use/'




for file in os.listdir(srcfile):
    if file.endswith('.xml'):
    	name=file.strip().split('_')
    	if len(name)>2:
    		ori_file=name[0]+'_'+name[1]+'.xml'
    		filepath=os.path.join(srcfile,file)
    		ori_filepath=os.path.join(srcfile,ori_file)
    		shutil.copy(ori_filepath,filepath)




