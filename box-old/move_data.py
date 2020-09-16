import os,shutil
import time
import cv2
import json

srcfile='./'
dstfile='../huawei_mix/'

def read_json(inputdir,outputdir):
	lines=[line for line in open(inputdir,'r')]
	for line in lines:
		json_data=line.strip().split('================')[1]
		dict_data=json.loads(json_data)
		wcs_list=dict_data[0]['value']

		fp = open(outputdir,'w')

		for wcs in wcs_list:
			fp.write(str(wcs['length']))
			fp.write(' ')
			fp.write(str(wcs['width']))
			fp.write(' ')
			fp.write(str(wcs['height']))
			fp.write(' ')
			fp.write('\n')

def find_by_time(dst_paths,dst_paths_time,mtime):
	
	res=''
	num=-1
	for i in range(len(dst_paths_time)):
		proc_time=mtime-dst_paths_time[i]
		if proc_time>=0 and proc_time<10:			
			res=dst_paths[i]
			num=i
			break
	if num!=-1:
		del dst_paths_time[num]
		del dst_paths[num]
	return res


if __name__=='__main__':

	for dir_name in os.listdir(srcfile):		
		#calcu .png files path for one dir
		dir_path=srcfile+dir_name
		dst_paths=[]
		if os.path.isdir(dir_path):
			for file in os.listdir(dir_path):
				file_path=os.path.join(dir_path,file)
				if os.path.isdir(file_path) and file!='data':
					for dst_file in os.listdir(file_path):
						if dst_file.endswith('.png'):
							dst_path = os.path.join(file_path,dst_file)
							dst_paths.append(dst_path)

			#calcu change time
			dst_paths_time=[]
			for dst_path in dst_paths:
				mtime = os.stat(dst_path).st_mtime
				dst_paths_time.append(mtime)

			#for different type files solve
			current_dst_path=''			
			dst_files=os.listdir(dir_path)
			for i in range(len(dst_files)):
				file_path=os.path.join(dir_path,dst_files[i])

				if not os.path.isdir(file_path):
					if file_path.endswith('.txt'):
						if i+1<len(dst_files):
							file_path2=os.path.join(dir_path,dst_files[i+1])
						else:
							file_path2=file_path
						if not file_path2.endswith('.txt'):
							out_dir_path=dstfile+dst_files[i].strip().split('.')[0]
							if not os.path.exists(out_dir_path):
								os.mkdir(out_dir_path)
							current_dst_path=out_dir_path

							wcs_path=out_dir_path+'/wcs.txt'
							read_json(file_path,wcs_path)
					if file_path.endswith('.png'):

						# print(current_dst_path)

						if current_dst_path=='':
							continue
						mtime = os.stat(file_path).st_mtime
						src_file_path=find_by_time(dst_paths,dst_paths_time,mtime)
						if src_file_path=='':
							print('find failed!')
							print(file_path)
							continue
						dst_file_path=os.path.join(current_dst_path,dst_files[i])

						src_cld_path=src_file_path.replace('.png','.cld')
						dst_cld_path=dst_file_path.replace('.png','.cld')

						src_detect_path=file_path
						dst_detect_path=current_dst_path+'/'+dst_files[i].split('.')[0]+'_detect.png'


						try:
							if os.path.exists(dst_file_path) and os.path.exists(dst_cld_path) and os.path.exists(dst_detect_path):
								continue
							shutil.copy(src_file_path,dst_file_path)
							shutil.copy(src_cld_path,dst_cld_path)
							# shutil.copy(src_detect_path,dst_detect_path)
							img=cv2.imread(src_detect_path)
							img=cv2.resize(img,(400,400))
							cv2.imwrite(dst_detect_path,img)

							print(src_file_path)
							print('rest data:')
							print(len(dst_files)-i)
							# shutil.move(move_path1,move_path2)
						except:
							print('copy failed!')
							print(src_file_path)
							print(src_cld_path)
							print(src_detect_path)
							continue





















						
# test ='E:/data/HUAWEI_ALL_DATA_cld/1210_data/2019-12-09_14-40-33.png'
# test_out ='E:/data/HUAWEI_ALL_DATA_cld/1210_data/2019-12-09_14-40-33_detect.png'
# test_txt ='E:/data/HUAWEI_ALL_DATA_cld/1210_data/2019-12-09_14-40-27.txt'
# test_txt_out ='E:/data/HUAWEI_ALL_DATA_cld/1210_data/wcs.txt'
# mtime = os.stat(test).st_mtime
# file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
# print(file_modify_time)
# print(mtime)
# img=cv2.imread(test)
# img=cv2.resize(img,(400,400))
# cv2.imwrite(test_out,img)
# xx=[1,2,34,5]
# def test(input):

# 	for i in input:
# 		if i==34:
# 			input.remove(i)
# test(xx)
# print(xx)

# lines=[line for line in open(test_txt,'r')]
# for line in lines:
# 	json_data=line.strip().split('================')[1]
# 	dict_data=json.loads(json_data)
# 	wcs_list=dict_data[0]['value']

# 	fp = open(test_txt_out,'w')
# 	print(test_txt_out)

# 	for wcs in wcs_list:
# 		fp.write(str(wcs['length']))
# 		fp.write(' ')
# 		fp.write(str(wcs['width']))
# 		fp.write(' ')
# 		fp.write(str(wcs['height']))
# 		fp.write(' ')
# 		fp.write('\n')    

