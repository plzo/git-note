import time
import numpy as np
import json
import open3d
import cv2
from enum import Enum
from clipper import *
from pyBoxDetector import BoxDetector

class TestObject:
    def __init__(self):
        self.corners2d = []
        self.corners3d = []
        self.length = 0
        self.width = 0
        self.center = np.zeros(3)
        self.normal = np.zeros(3)
        self.score = -1

class CheckResult(Enum):
    unknown = 0
    wrong = 1
    warning = 2
    accepted = 3

def fitPlane(points):
    b = np.ones([1, points.shape[0]])
    m = np.concatenate((points, b.T), axis=1)
    U, s, V = np.linalg.svd(m, full_matrices=False)
    coeffs = V[3]
    return coeffs.T

def getPlaneCoeffRansac(points, n=50, k=30, t=0.01, d=1000):
    n = int(n)
    iterations = 0
    bestFit = None
    bestErr = 1e10
    while iterations < k:
        # select random points
        points_idx = np.arange(points.shape[0])
        np.random.shuffle(points_idx)
        random_idx_selected = points_idx[:n]
        random_idx_others = points_idx[n:]
        maybeInliers = points[random_idx_selected]
        # get a model fitting these points
        maybeModel = fitPlane(maybeInliers)
        # alsoInliers
        alsoInliers = []
        otherpoints = points[random_idx_others]
        otherpoints_H = np.concatenate((otherpoints, np.ones([1, otherpoints.shape[0]]).T), axis=1)
        alsoInliers = otherpoints[np.abs(otherpoints_H.dot(maybeModel.T)) < t]
        if alsoInliers.shape[0] > d:
            inliers = np.concatenate((maybeInliers, alsoInliers), axis=0)
            betterModel = fitPlane(inliers)
            inliers_H = np.concatenate((inliers, np.ones([1, inliers.shape[0]]).T), axis=1)
            # err is the number of outliers
            thisErr = points.shape[0] - inliers.shape[0]
            if thisErr < bestErr:
                bestFit = betterModel
                bestErr = thisErr
        iterations = iterations + 1
    return bestFit

class BoxDetectorTest:
    def __init__(self, model_file_str, trained_file_str, param):
        param_json = json.dumps(param)
        self.camera_K = np.array([[param["camera"]["fx"], 0, param["camera"]["cx"]], [0, param["camera"]["fy"], param["camera"]["cy"]], [0, 0, 1]])
        self.box_detector = BoxDetector(model_file_str, trained_file_str, param_json, [104, 117, 123])
        self.iou_threshold = 0.1
        self.warning_iou_threshold = 0.75
        self.accept_iou_threshold = 0.9
        self.accept_center_distance = 0.01
        self.warning_center_distance = 0.03
        self.accept_z_distance = 0.01
        self.warning_z_distance = 0.01
        self.totalTime = 0.0
        self.box_detector.saveResultEachPhase(True)
    
    def test(self, input_image_file, input_cloud_file, input_boxes, gt_label_file):
        # run test
        self.image = cv2.imread(input_image_file)
        self.cloud = open3d.read_point_cloud(input_cloud_file)
        t0 = time.clock()
        results = self.box_detector.detect(input_image_file, input_cloud_file, input_boxes)
        self.totalTime = self.totalTime + (time.clock() - t0)

        # save output results. set corners2d, corners3d, length, width, center
        self.output_objects = [None] * len(results)
        for i in range(len(results)):
            self.output_objects[i] = TestObject()
            output_corners3d = np.array(results[i].corners).transpose()
            tmp = self.camera_K.dot(output_corners3d)
            output_corners2d = (tmp / tmp[2]).transpose()
            self.output_objects[i].corners3d = results[i].corners
            self.output_objects[i].corners2d = np.int32(output_corners2d[:,:2])
            self.output_objects[i].length = results[i].length
            self.output_objects[i].width = results[i].width
            self.output_objects[i].center = results[i].center
            self.output_objects[i].score = results[i].score

        # read ground truth file to get rect corners, centers
        label = self.__readLabelFile(gt_label_file)
        # save ground truth objects. set corners2d, center
        self.gt_objects = [None] * len(label["shapes"])
        if len(label["shapes"]) > 0:
            for i in range(len(label["shapes"])):
                self.gt_objects[i] = TestObject()
                self.gt_objects[i].corners2d = np.float32(label["shapes"][i]["points"])
                self.gt_objects[i].corners3d = label["shapes"][i]["corners3d"]
                self.gt_objects[i].center = label["shapes"][i]["center"]
                self.gt_objects[i].normal = label["shapes"][i]["normal"]
                self.gt_objects[i].length = label["shapes"][i]["length"]
                self.gt_objects[i].width = label["shapes"][i]["width"]
        
        
        # for i in self.gt_objects:
        #     print(i.corners2d, i.corners3d, i.center)
        
        # for i in self.output_objects:
        #     print(i.corners2d, i.corners3d, i.length, i.width, i.center)
    
    def visualization(self):
        img = self.image.copy()
        for rect in self.gt_rects:
            for i in range(4):
                cv2.line(img, tuple(rect[i]), tuple(rect[(i+1)%4]), (255, 0, 0), 4)
        for rect in self.output_rects:
            for i in range(4):
                cv2.line(img, tuple(rect[i]), tuple(rect[(i+1)%4]), (0, 255, 0), 4)
        show_image = cv2.resize(img, (0,0), fx=0.3, fy=0.3)
        return show_image
    
    def checkHighest(self):
        gt_box_num = len(self.gt_objects)
        # get highest box(es)
        highest_value = 99999
        for i in range(len(self.gt_objects)):
            if highest_value > self.gt_objects[i].center[2]:
                highest_value = self.gt_objects[i].center[2]
        gt_highest_obj_idx = []
        for i in range(len(self.gt_objects)):
            if self.gt_objects[i].center[2] < highest_value + 0.05:
                gt_highest_obj_idx.append(i)
        
        # find an output object fits to each highest object
        highest_match_idx = []
        for i in gt_highest_obj_idx:
            max_iou = -1
            max_iou_idx = -1
            for j in range(len(self.output_objects)):
                iou = self.__iou(self.output_objects[j].corners2d, self.gt_objects[i].corners2d)
                if iou > max_iou:
                    max_iou = iou
                    max_iou_idx = j
            if max_iou > self.iou_threshold:
                highest_match_idx.append((max_iou_idx, max_iou))
            else:
                highest_match_idx.append((-1,0))
        
        # check output object
        self.checkHighestResult = []
        for i in range(len(gt_highest_obj_idx)):
            result = CheckResult.wrong
            if highest_match_idx[i][0] < 0:
                result = CheckResult.unknown
            else:
                centerdist = self.gt_objects[gt_highest_obj_idx[i]].center - self.output_objects[highest_match_idx[i][0]].center
                dist = np.linalg.norm(centerdist)
                if highest_match_idx[i][1] > self.accept_iou_threshold and dist < self.accept_center_distance:
                    result = CheckResult.accepted
                elif dist < self.warning_center_distance and highest_match_idx[i][1] > self.warning_iou_threshold:
                    result = CheckResult.warning
                else:
                    result = CheckResult.wrong
            self.checkHighestResult.append((gt_highest_obj_idx[i], highest_match_idx[i][0], result))
        
        self.checkHighestPass = False
        # if there are not any gt boxes, AC
        if len(self.checkHighestResult) == 0:
            self.checkHighestPass = True
        # if one of gt 
        # if one of gt is recognized out, AC
        for t in self.checkHighestResult:
            if t[2] == CheckResult.accepted or t[2] == CheckResult.warning:
                self.checkHighestPass = True
            if t[2] == CheckResult.wrong:
                self.checkHighestPass = False
                break

    def highestCheckVisualize(self):
        img_origin = self.image.copy()
        img_draw = self.image.copy()
        for t in self.checkHighestResult:
            gt_rect = np.int32(self.gt_objects[t[0]].corners2d)
            if t[1] >= 0:
                output_rect = self.output_objects[t[1]].corners2d
                #draw output
                if t[2] == CheckResult.accepted:
                    color = (0, 255, 0)
                    cv2.fillPoly(img_draw, [np.int32((tuple(output_rect[0]), tuple(output_rect[1]), tuple(output_rect[2]), tuple(output_rect[3])))], color)
                elif t[2] == CheckResult.warning:
                    color = (0, 255, 255)
                    cv2.fillPoly(img_draw, [np.int32((tuple(output_rect[0]), tuple(output_rect[1]), tuple(output_rect[2]), tuple(output_rect[3])))], color)
                elif t[2] == CheckResult.wrong:
                    color = (0, 0, 255)
                    cv2.fillPoly(img_draw, [np.int32((tuple(output_rect[0]), tuple(output_rect[1]), tuple(output_rect[2]), tuple(output_rect[3])))], color)
            #draw gt
            for i in range(4):
                cv2.line(img_draw, tuple(gt_rect[i]), tuple(gt_rect[(i+1)%4]), (255, 0, 0), 5)
        show_image = cv2.addWeighted(img_origin, 0.8, img_draw, 0.2, 0)
        show_image = cv2.resize(show_image, (0,0), fx=0.5, fy=0.5)
        return show_image

    def checkAccuracy(self):
        output_box_num = len(self.output_objects)
        match_idx = []
        for i in range(output_box_num):
            max_iou = -1
            max_iou_idx = -1
            for j in range(len(self.gt_objects)):
                iou = self.__iou(self.output_objects[i].corners2d, self.gt_objects[j].corners2d)
                if iou > max_iou:
                    max_iou = iou
                    max_iou_idx = j
            if max_iou > self.iou_threshold:
                match_idx.append((max_iou_idx, max_iou))
            else:
                match_idx.append((-1, 0))
        
        # check output object
        self.checkAccuracyResult = []
        for i in range(output_box_num):
            result = CheckResult.wrong
            if match_idx[i][0] < 0:
                result = CheckResult.unknown
            else:
                centerdist = np.array(self.gt_objects[match_idx[i][0]].center) - np.array(self.output_objects[i].center)
                #dist = np.linalg.norm(centerdist)
                dist = np.sqrt(centerdist[0]*centerdist[0]+centerdist[1]*centerdist[1])
                if match_idx[i][1] > self.accept_iou_threshold and dist < self.accept_center_distance:
                    result = CheckResult.accepted
                elif dist < self.warning_center_distance and match_idx[i][1] > self.warning_iou_threshold:
                    result = CheckResult.warning
                else:
                    result = CheckResult.wrong
                    if match_idx[i][1] < self.warning_iou_threshold:
                        print("iou = ", match_idx[i][1])
                    if dist > self.warning_center_distance:
                        print("dist = ", dist)

            self.checkAccuracyResult.append((i, match_idx[i][0], result))
        

        self.checkAccuracyPass = False
        # if there are not any gt boxes, AC
        if len(self.checkAccuracyResult) == 0:
            self.checkAccuracyPass = True
        # if one of gt 
        # if one of gt is recognized out, AC
        for t in self.checkAccuracyResult:
            if t[2] == CheckResult.accepted or t[2] == CheckResult.warning:
                self.checkAccuracyPass = True
            if t[2] == CheckResult.wrong or t[2] == CheckResult.unknown:
                self.checkAccuracyPass = False
                break
    
    def accuracyCheckVisualize(self):
        img_origin = self.image.copy()
        img_draw = self.image.copy()
        for t in self.checkAccuracyResult:

            output_rect = self.output_objects[t[0]].corners2d
            #draw output
            if t[2] == CheckResult.accepted:
                color = (0, 255, 0)
                cv2.fillPoly(img_draw, [np.int32((tuple(output_rect[0]), tuple(output_rect[1]), tuple(output_rect[2]), tuple(output_rect[3])))], color)
            elif t[2] == CheckResult.warning:
                color = (0, 255, 255)
                cv2.fillPoly(img_draw, [np.int32((tuple(output_rect[0]), tuple(output_rect[1]), tuple(output_rect[2]), tuple(output_rect[3])))], color)
            elif t[2] == CheckResult.wrong:
                color = (0, 0, 255)
                cv2.fillPoly(img_draw, [np.int32((tuple(output_rect[0]), tuple(output_rect[1]), tuple(output_rect[2]), tuple(output_rect[3])))], color)
            elif t[2] == CheckResult.unknown:
                color = (0, 0, 255)
                cv2.fillPoly(img_draw, [np.int32((tuple(output_rect[0]), tuple(output_rect[1]), tuple(output_rect[2]), tuple(output_rect[3])))], color)
        #draw gt
        
        for i in range(len(self.gt_objects)):
            gt_rect = self.gt_objects[i].corners2d
            for j in range(4):
                cv2.line(img_draw, tuple(gt_rect[j]), tuple(gt_rect[(j+1)%4]), (255, 0, 0), 3)
        show_image = cv2.addWeighted(img_origin, 0.8, img_draw, 0.2, 0)
        show_image = cv2.resize(show_image, (0,0), fx=0.5, fy=0.5)
        return show_image
    
    def check_score_iou(self):
        output_box_num = len(self.output_objects)
        match_idx = []
        ans = []
        for i in range(output_box_num):
            max_iou = -1
            max_iou_idx = -1
            for j in range(len(self.gt_objects)):
                iou = self.__iou(self.output_objects[i].corners2d, self.gt_objects[j].corners2d)
                if iou > max_iou:
                    max_iou = iou
                    max_iou_idx = j
            if max_iou > self.iou_threshold:
                match_idx.append((max_iou_idx, max_iou))
            else:
                match_idx.append((-1, 0))
            ans.append([self.output_objects[i].score, max_iou])
        return ans
    
    def getPhaseResult(self):
        return np.array(self.box_detector.pyGetPhaseResult(), dtype=np.uint8)
    
    def __readLabelFile(self, filename):
        label_file = open(filename)
        label_json = label_file.read()
        label = json.loads(label_json)
        #print(label)
        if "imageData" in label:
            del(label["imageData"])
        return label

    def __isInRect(self, p, rect):
        affine = cv2.getAffineTransform(rect[:3], np.float32([[0.0,0.0], [1.0,0.0], [1.0,1.0]]))
        img_p = affine.dot(np.float32([p[0], p[1], 1]))
        return img_p[0] >= 0 and img_p[0] <= 1 and img_p[1] >= 0 and img_p[1] <= 1

    def __getBoxPoints3d(self, rects, K, points):
        points = points.transpose()
        img_points = K.dot(points)
        img_points = (img_points / img_points[2]).transpose()
        affines = []
        for rect in rects:
            affine = cv2.getAffineTransform(rect[:3], np.float32([[0.0,0.0], [1.0,0.0], [1.0,1.0]]))
            affines.append(affine)
        affines = np.array(affines)
        np.moveaxis(affines, 0, -1)
        newpoints = affines.dot(img_points.transpose())
        newpoints = np.moveaxis(newpoints, 1, -1)
        boxid = np.logical_and((newpoints[:,:] >= 0), (newpoints[:,:] <= 1))
        return np.logical_and(boxid[:,:,0], boxid[:,:,1])

    def __getPlaneCoeff(self, points):
        b = np.ones([1, points.shape[0]])
        m = np.concatenate((points, b.T), axis=1)
        U, s, V = np.linalg.svd(m, full_matrices=False)
        coeffs = V[3]
        return coeffs
    
    def __get3dpoint(self, K, point2d, planecoeff):
        point3d_h = np.linalg.inv(K).dot(np.array([[point2d[0]], [point2d[1]], [1]]))
        t = -planecoeff[3] / planecoeff[:3].dot(point3d_h)
        point3d = t * point3d_h
        return point3d.transpose()[0]
    
    def __iou(self, rect1, rect2):
        rect1_path, rect2_path = [], []
        for p in rect1:
            rect1_path.append(Point(p[0], p[1]))
        for p in rect2:
            rect2_path.append(Point(p[0], p[1]))

        rect1_paths = [rect1_path]
        rect2_paths = [rect2_path]

        solution = []
        pft = PolyFillType.EvenOdd
        c = Clipper()
        c.AddPolygons(rect1_paths, PolyType.Subject)
        c.AddPolygons(rect2_paths, PolyType.Clip)
        result = c.Execute(ClipType.Intersection, solution, pft, pft)
        if len(solution) == 0:
            return 0
        intersection_area = Area(solution[0])
        result = c.Execute(ClipType.Union, solution, pft, pft)
        union_area = Area(solution[0])
        return intersection_area / union_area
    
        