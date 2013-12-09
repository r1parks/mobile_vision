#!/usr/bin/env python

import sys
import cv2

search_for = sys.argv[1]

print "{0}".format(filter(lambda x: search_for in x, dir(cv2)))
print "cv.{0}".format(filter(lambda x: search_for in x, dir(cv2.cv)))
