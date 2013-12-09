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
    return blurred_diff

if __name__ == "__main__":
    vid = cv2.VideoCapture(filename)
    assert(vid.isOpened())

    height = int(vid.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    width = int(vid.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))

    new_video = cv2.VideoWriter("diff_vid.mpg", cv2.cv.CV_FOURCC('M', 'P', 'E', 'G'), 24, (width, height), 1)

    saved_frames = []
    status, next_frame = get_next_frame(vid)
    assert(status)
    saved_frames.append(next_frame)

    for _ in range(diff_len):
        status, next_frame = get_next_frame(vid)
        assert(status)
        saved_frames.append(next_frame)

    while status:
        status, next_frame = get_next_frame(vid)
        if not status:
            break
        diff = get_diff_img(saved_frames[0], next_frame)
        output_frame = cv2.add(next_frame, diff)
        saved_frames = saved_frames[1:]
        saved_frames.append(next_frame)
        new_video.write(output_frame)
        cv2.namedWindow("diff_view")
        cv2.imshow("diff_view", output_frame)
        cv2.waitKey(25)

    print "Program is done :)"
