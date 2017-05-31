import cv2
import numpy as np
params = cv2.SimpleBlobDetector_Params()
# Change thresholds
params.minThreshold = 10;
params.maxThreshold = 200;
 
# Filter by Area.
params.filterByArea = True
params.minArea = 1500
 
# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1
 
# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.87
 
# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01

blobVer = (cv2.__version__).split('.')
if int(blobVer[0]) < 3:
    detector = cv2.SimpleBlobDetector(params)
else:
    detector = cv2.SimpleBlobDetector_create(params)
    
frame = cv2.imread("BlobTest.jpg",cv2.IMREAD_GRAYSCALE)

keypoints = detector.detect(255 - frame)
len(keypoints)
for keypoint in keypoints:
    print(keypoint.pt[0],keypoint.pt[1],keypoint.size)
im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("foo",im_with_keypoints)
while True:
    c = cv2.waitKey(0)
    if  c == -1:
        break
cv2.destroyAllWindows()

"""
print("out")
keypoints = detector.detect(frame)
print(keypoints)
"""
