#!/usr/bin/env python

import cv2
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

vid = cv2.VideoCapture(filename)
assert(vid.isOpened())

height = int(vid.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
width = int(vid.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))

new_video = cv2.VideoWriter("diff_vid.mpg", cv2.cv.CV_FOURCC('M', 'P', 'E', 'G'), 24, (width, height), 1)

status, next_frame = get_next_frame(vid)

while status:
    if not status:
        break
    new_video.write(next_frame)
    cv2.namedWindow("diff_view")
    cv2.imshow("diff_view", next_frame)
    cv2.waitKey(25)
    status, next_frame = get_next_frame(vid)

print "Program is done :)"

