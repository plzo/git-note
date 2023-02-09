import os,shutil
srcfile='./'

for file in os.listdir(srcfile):
	sub_path=srcfile+file
	if os.path.isdir(sub_path):
		for sub_file in os.listdir(sub_path):
			if sub_file=='wcs.txt' or sub_file=='camera_param.txt':
				continue
			if len(sub_file.strip().split('_'))==2:
				continue
			file_name=file+'_'+sub_file
			move_path1=os.path.join(sub_path,sub_file)
			move_path2=os.path.join(sub_path,file_name)
			# shutil.copy(move_path1,move_path2)
			shutil.move(move_path1,move_path2)
    




