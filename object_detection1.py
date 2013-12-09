#!/usr/bin/env python

import cv2
import time
import sys
import numpy

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
        line_color = cv2.cv.CV_RGB(255,0,0)
        output_img = numpy.copy(frame2)
        for i in range(len(imgfeatures1)):
            cv2.line(output_img, (imgfeatures1[i][0][0], imgfeatures1[i][0][1]), (next_points[i][0][0], next_points[i][0][1]), line_color, 3)
        cv2.namedWindow("OpticalFlow")
        cv2.imshow("OpticalFlow", output_img)
        cv2.waitKey(1)
        frame1 = frame2
        status, frame2 = get_next_frame(vid)
