#!/usr/bin/env python

import cv2
import numpy
import time
import sys

filename = "pepsi_truck.mp4"

def get_next_frame(vid):
    status, frame = vid.read()
    if not status:
        return status, frame
    return status, rotate_frame(frame)

def rotate_frame(frame):
    return cv2.flip(cv2.transpose(frame), 1)

diff_len = 1
try:
    diff_len = int(sys.argv[1])
except:
    pass

def get_diff_img(frame1, frame2):
    diff = cv2.subtract(frame1, frame2)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blurred_gray_diff = cv2.blur(gray_diff, (11,11))
    blurred_diff = cv2.cvtColor(blurred_gray_diff, cv2.COLOR_GRAY2RGB)
    threshold_diff = cv2.threshold(blurred_gray_diff, 70, 255, cv2.THRESH_BINARY)
    blurred_diff = cv2.cvtColor(threshold_diff[1], cv2.COLOR_GRAY2RGB)
    return blurred_diff

def add_optical_flow_vectors(output_img, pts1, pts2):
    line_color = cv2.cv.CV_RGB(255,0,0)
    line_width = 4
    for i in range(len(imgfeatures1)):
        pt1 = (imgfeatures1[i][0][0], imgfeatures1[i][0][1])
        pt2 = (next_points[i][0][0], next_points[i][0][1])
        vector = (abs(pt1[0] - pt2[0]), abs(pt1[1] - pt2[1]))
        magnitude = vector[0] ** 2 + vector[1] ** 2
        if magnitude > 30.0:
            cv2.line(output_img, pt1, pt2, line_color, line_width)

def find_points_of_interest(pts1, pts2):
    interesting_points = []
    for i in range(len(pts1)):
        pt1 = (imgfeatures1[i][0][0], imgfeatures1[i][0][1])
        pt2 = (next_points[i][0][0], next_points[i][0][1])
        vector = (abs(pt1[0] - pt2[0]), abs(pt1[1] - pt2[1]))
        magnitude = vector[0] ** 2 + vector[1] ** 2
        if magnitude > 30.0:
            interesting_points.append(pt2)
    return interesting_points

def do_clustering(cluster_points):
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 1, 10)
    retval, bestLabels, centers = cv2.kmeans(cluster_points, 
                                             K=7, 
                                             bestLabels=None, 
                                             criteria=criteria, 
                                             attempts=1, 
                                             flags=cv2.KMEANS_RANDOM_CENTERS)
    return retval, bestLabels, centers

def add_clustering_points(img, points, labels, centers):
    colors = [cv2.cv.CV_RGB(255,0,0),
              cv2.cv.CV_RGB(0,255,0),
              cv2.cv.CV_RGB(0,0,255),
              cv2.cv.CV_RGB(255,255,0),
              cv2.cv.CV_RGB(255,0,255),
              cv2.cv.CV_RGB(0,255,255),
              cv2.cv.CV_RGB(255,255,255)]
    for (point, label) in zip(points, labels):
        cv2.circle(img, (point[0], point[1]), 4, colors[label[0]], thickness = -1)

def add_object_edges(input_img, output_img, points):
    edges = cv2.Canny(input_img, 200, 350)
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    for point in points:
        cv2.circle(output_img, (point[0], point[1]), 40, cv2.cv.CV_RGB(255,255,255), thickness=-1)
    import pdb; pdb.set_trace()

if __name__ == "__main__":
    vid = cv2.VideoCapture(filename)
    assert(vid.isOpened())
    height = int(vid.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    width = int(vid.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    status, frame1 = get_next_frame(vid)
    assert(status)
    status, frame2 = get_next_frame(vid)
    assert(status)
    number_of_corners = 100
    quality_level = 0.01
    min_distance = 5
    max_level = 0
    while status:
        gray_frame1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
        gray_frame2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
        imgfeatures1 = cv2.goodFeaturesToTrack(gray_frame1, number_of_corners, quality_level, min_distance)
        next_points, status, err = cv2.calcOpticalFlowPyrLK(gray_frame1, gray_frame2, imgfeatures1, maxLevel=max_level)
        blank_img = numpy.copy(frame1)
        blank_img[:] = 0
        optical_flow_img = numpy.copy(blank_img)
        add_optical_flow_vectors(optical_flow_img, imgfeatures1, next_points)
        _, labels, centers = do_clustering(next_points.astype('float32'))
        points_of_interest = find_points_of_interest(imgfeatures1, next_points)
        clustering_img = numpy.copy(blank_img)
        add_clustering_points(clustering_img, points_of_interest, labels, centers)
        edges_img = numpy.copy(blank_img)
        add_object_edges(frame2, edges_img, points_of_interest)
        cv2.namedWindow("OpticalFlow")
        #cv2.imshow("OpticalFlow", optical_flow_img + clustering_img + edges_img + frame2)
        cv2.imshow("OpticalFlow", edges_img)
        cv2.waitKey(1)
        frame1 = frame2
        status, frame2 = get_next_frame(vid)

