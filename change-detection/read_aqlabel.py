import os
import sys
import json
sys.path.insert(0,'D:/yang.xie/packages')
from aidi410_label.aidi_vision import *


def get_name_score(one_label_path):
	in_label = LabelIO()
	in_label.read_from(one_label_path)
	tmp = in_label.to_json()
	json_label = json.loads(tmp)
	return json_label['regions'][0]['name'],json_label['regions'][0]['score']


if __name__=="__main__":
    one_label_path = './1.aqlabel'
    get_name_score()