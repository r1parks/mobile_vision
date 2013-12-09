import cv
import cv2
import numpy as np
import numpy.random as r


samples = cv.CreateMat(50, 2, cv.CV_32FC1)
random_points = r.multivariate_normal((100,100), np.array([[150,400],[150,150]]), size=(25))
random_points_2 = r.multivariate_normal((300,300), np.array([[150,400],[150,150]]), size=(25))   
samples_list = np.append(random_points, random_points_2).reshape(50,2)  
random_points_list = np.array(samples_list, np.float32) 
samples = cv.fromarray(random_points_list)

blank_image = np.zeros((400,400,3))
blank_image_classified = np.zeros((400,400,3))

for point in random_points_list:
    cv2.circle(blank_image, (int(point[0]),int(point[1])), 1, (0,255,0),-1)

import pdb; pdb.set_trace()
temp, classified_points, means = cv2.kmeans(data=np.asarray(samples), K=2, bestLabels=None,
criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 1, 10), attempts=1, 
flags=cv2.KMEANS_RANDOM_CENTERS)   #Let OpenCV choose random centers for the clusters

for point, allocation in zip(random_points_list, classified_points):
    if allocation == 0:
        color = (255,0,0)
    elif allocation == 1:
        color = (0,0,255)
    cv2.circle(blank_image_classified, (int(point[0]),int(point[1])), 1, color,-1)

cv2.imshow("Points", blank_image)
cv2.imshow("Points Classified", blank_image_classified)
cv2.waitKey()
