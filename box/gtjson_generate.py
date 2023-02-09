import json
import numpy as np
import open3d
import cv2

param = {"roi_3d":{"qw":1.0,"qx":0.0,"qy":0.0,"qz":0.0,"tx":0.0,"ty":0.0,"tz":0.0,"minx":-0.65, "miny":-0.65, "minz":1.60, "maxx":0.65, "maxy":0.65, "maxz":3.1}, 
         "camera":{"distortion_type":"No Distortion", "fx":2328.24, "fy":2329.54, "cx":1217.36, "cy":978.34, "height":2048, "width":2448}}
input_dir = "D:/data/nongfushanquan/testdata/"

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

def backProject(K, point2d, planecoeff):
    point3d_h = np.linalg.inv(K).dot(np.array([[point2d[0]], [point2d[1]], [1]]))
    t = -planecoeff[3] / planecoeff[:3].dot(point3d_h)
    point3d = t * point3d_h
    return point3d.transpose()[0]

def projectInRects(rects, K, points):
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

def readLabelFile(filename):
    label_file = open(filename)
    label_json = label_file.read()
    label = json.loads(label_json)
    #print(label)
    if "imageData" in label:
        del(label["imageData"])
    return label

def generateGroundTruthJSON(input_json_file, input_pcd_file, camera_K):
    label = readLabelFile(input_json_file)
    cloud = open3d.read_point_cloud(input_pcd_file)
    cloud_points_array = np.asarray(cloud.points)
    rect_corners2d = []
    
    if len(label["shapes"]) == 0:
        return json.dumps(label)
        

    for polygon in label["shapes"]:
        corners2d = np.float32(polygon["points"])
        rect_corners2d.append(corners2d)
        
    cluster_select = projectInRects(rect_corners2d, camera_K, cloud_points_array)
    index = 0
    for polygon in label["shapes"]:
        points = cloud_points_array[cluster_select[index]]
        plane_coeffs = getPlaneCoeffRansac(points)
        corners3d = []
        for j in range(4):
            point3d = backProject(camera_K, rect_corners2d[index][j], plane_coeffs).tolist()
            corners3d.append(point3d)
        polygon["corners3d"] = corners3d
        polygon["center"] = np.mean(corners3d, axis=0).tolist()
        polygon["normal"] = (plane_coeffs[:3] / np.linalg.norm(plane_coeffs[:3])).tolist()
        length_v = np.array(corners3d[0]) - np.array(corners3d[1])
        width_v = np.array(corners3d[1]) - np.array(corners3d[2])
        length = np.linalg.norm(length_v)
        width = np.linalg.norm(width_v)
        if width > length:
            length, width = width, length
        polygon["length"] = length
        polygon["width"] = width
        index = index+1
    return json.dumps(label)

if __name__ == '__main__':
    for i in range(83, 178):
        camera_K = np.array([[param["camera"]["fx"], 0, param["camera"]["cx"]], [0, param["camera"]["fy"], param["camera"]["cy"]], [0, 0, 1]])
        input_json_file = input_dir + str(i) + ".json"
        input_pcd_file = input_dir + str(i) + ".pcd"

        gt_json = generateGroundTruthJSON(input_json_file, input_pcd_file, camera_K)

        f = open(input_dir + str(i) + "_gt.json", "w")
        f.write(gt_json)
        f.close()
        print("write", input_dir + str(i) + "_gt.json")
