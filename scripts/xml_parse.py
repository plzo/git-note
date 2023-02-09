import os
import sys
import random,shutil

import xml.dom.minidom

def parse_xml(xml_file):
	dom = xml.dom.minidom.parse(xml_file)
	root = dom.documentElement
	defect_num = root.getElementsByTagName('DefectNum')[0].childNodes[0].data
	list_0 = []
	list_1 = []
	list_2 = []
	list_3 = []
	for index in range(int(defect_num)):
		name = 'Defect' + str(index)
		defect_name_level = root.getElementsByTagName(name)[0].childNodes[0].data
		defect_name = defect_name_level.strip().split('-')[0]
		defect_level = defect_name_level.strip().split('-')[1]
		if defect_level == '放行':
			list_0.append(defect_name)
		elif defect_level == '轻度':
			list_1.append(defect_name)
		elif defect_level == '中度':
			list_2.append(defect_name)
		else:
			list_3.append(defect_name)
	return list_0,list_1,list_2,list_3



if __name__ == '__main__':
	xml_file = 'D:/yang.xie/workspace/defects.xml'
	print(parse_xml(xml_file))



					



