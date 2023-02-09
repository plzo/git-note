import os
import sys
import xmltodict
from collections import OrderedDict
from xml.dom.minidom import Document
import json
import cv2
import numpy as np

def parse_annotation(xml_path):
    with open(xml_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = xmltodict.parse(f.read())

    boxes = []
    occluded = []
    sides = []

    # print(content)
    objects = content.get('annotation', {}).get('object', [])
    if isinstance(objects, (dict, OrderedDict)):
        objects = [objects]
    # for anno in dict(content.get('annotation', {})).get('object', []):
    for anno in objects:
        # print([dict(content.get('annotation', {})).get('object', []), anno])
        name = anno.get('name', '').strip().lower()
        attribute = anno.get('attribute', '').strip().lower()
        polygon = anno.get('polygon', {}).get('point', [])
        polygon = [[int(_['x']), int(_['y'])] for _ in polygon]

        # deduplicate
        polygon_ = []
        for pt1 in polygon:
            skip = False
            for pt2 in polygon_:
                if ((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2) < 25:
                    skip = True
                    break
            if not skip:
                polygon_.append(pt1)

        polygon = polygon_
        # print(name, attribute, polygon)

        if len(polygon) < 3:
            continue

        if attribute == 'occluded':
            occluded.append(polygon)
        elif 'side' in name + attribute:
            sides.append(polygon)
        elif len(polygon) == 4 \
                and (attribute == 'not occluded' or name == 'not occluded'):
            boxes.append(polygon)
        else:
            occluded.append(polygon)

    return [boxes, occluded, sides]

def parse_json(json_path):
    with open(json_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = json.load(f)
    boxes = [p['points'] for p in content['shapes']]
    anno = []

    # deduplicate
    for polygon in boxes:
        polygon_ = []
        for pt1 in polygon:
            skip = False
            for pt2 in polygon_:
                if ((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2) < 25:
                    skip = True
                    break
            if not skip:
                polygon_.append(pt1)
        polygon = polygon_
        if (len(polygon) == 4):
            anno.append(polygon)

    # keep an old style [boxes, occluded, sides]
    return [anno, [], []]

def write_xml(filepath, annos):
    doc = Document()
    annotation_node = doc.createElement('annotation')
    doc.appendChild(annotation_node)
    filename_node = doc.createElement('filename')
    filename_node.appendChild(doc.createTextNode(os.path.basename(filepath)))
    annotation_node.appendChild(filename_node)
    boxes = annos[0]

    for quad in boxes:
        assert(len(quad) == 4)
        object_node = doc.createElement('object')
        annotation_node.appendChild(object_node)

        name_node = doc.createElement('name')
        name_text = doc.createTextNode('Not Occluded')
        name_node.appendChild(name_text)

        object_node.appendChild(name_node)
        polygon_node = doc.createElement('polygon')
        object_node.appendChild(polygon_node)

        for point in quad:
            x_node = doc.createElement('x')
            x_node.appendChild(doc.createTextNode( str( int(round(point[0])) ) ))
            y_node = doc.createElement('y')
            y_node.appendChild(doc.createTextNode( str( int(round(point[1])) ) ))
            point_node = doc.createElement('point')
            point_node.appendChild(x_node)
            point_node.appendChild(y_node)
            polygon_node.appendChild(point_node)
    
    with open(os.path.splitext(filepath)[0] + '.xml', 'w+') as f:
        doc.writexml(f, indent='\t', addindent='\t', newl='\n', encoding="utf-8")

if __name__ == '__main__':
    if (len(sys.argv)) != 2:
        print('Needs a folder name.')
        sys.exit()
    dir_list = lambda dir_name :\
        [os.path.join(dir_name, p) \
        for p in os.listdir(dir_name) \
        if os.path.isfile(os.path.join(dir_name, p)) and p.endswith('.png') and not p.endswith('cloud.png')]
    image_list = dir_list(sys.argv[1])
    for filepath in image_list:
        filepath_noext = os.path.splitext(filepath)[0]
        annos = [[], [], []]
        if os.path.isfile(filepath_noext + '.json'):
            annos = parse_json(filepath_noext + '.json')
        write_xml(filepath, annos)

        print(filepath)

        # visulize annotation
        # img = cv2.imread(filepath)
        # short_side = 480
        # h, w = img.shape[:2]
        # scale_factor = 480. / min(h, w)
        # img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor)
        # annos = parse_annotation(filepath_noext + '.xml')
        # boxes = np.array(annos[0]) * scale_factor
        # if len(boxes) > 0:
        #     cv2.polylines(img, boxes.astype(np.int32), True, (0, 255, 0), 2, cv2.LINE_AA)
        # if not os.path.isdir(os.path.join(sys.argv[1], 'anno_vis')):
        #     os.mkdir(os.path.join(sys.argv[1], 'anno_vis'))
        # cv2.imwrite(os.path.join(sys.argv[1], 'anno_vis', os.path.basename(filepath)), img)