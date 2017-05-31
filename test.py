import cv2
import numpy as np;
 
# Read image
im = 255 - cv2.imread("Big_Dipper_l.jpg", cv2.IMREAD_GRAYSCALE)
im = cv2.erode(im,np.ones((6,6)))
# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()
 
# Change thresholds
params.minThreshold = 16;
params.maxThreshold = 81;
 
# Filter by Area.
params.filterByArea = True
params.minArea = 8
params.maxArea = 128
 
# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.4
params.maxCircularity = 1
 
# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.3
 
# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.5
 
# Create a detector with the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
    detector = cv2.SimpleBlobDetector(params)
else : 
    detector = cv2.SimpleBlobDetector_create(params)
 
# Detect blobs.
keypoints = detector.detect(im)
 
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
height, width = im_with_keypoints.shape[:2]
factor = 2.56
res = cv2.resize(im_with_keypoints,(int(factor*width), int(factor*height)), interpolation = cv2.INTER_CUBIC)
# Show keypoints
cv2.imshow("Keypoints", res)
cv2.waitKey(0)
quit()
