import cv2
import numpy as np
import time

def nothing(x):
    pass

class StarDetector:
    @staticmethod
    def getStarBlobs(im):
        im = cv2.erode(im,np.ones((2,2)))

        height, width = im.shape[:2]
        area = height * width
        # Setup SimpleBlobDetector parameters.
        params = cv2.SimpleBlobDetector_Params()
         
        # Change thresholds
        params.minThreshold = cv2.getTrackbarPos('minThr','image')
        params.maxThreshold = cv2.getTrackbarPos('maxThr','image')
         
        # Filter by Area.
        params.filterByArea = True
        #10000
        #500
        
        params.minArea = area/(cv2.getTrackbarPos('minAre','image') + 1)
        params.maxArea = area/(cv2.getTrackbarPos('maxAre','image') + 1)
         
        # Filter by Circularity
        params.filterByCircularity = True
        params.minCircularity = cv2.getTrackbarPos('minCir','image')
        params.maxCircularity = cv2.getTrackbarPos('maxCir','image')
         
        # Filter by Convexity
        params.filterByConvexity = False
        params.minConvexity = cv2.getTrackbarPos('minCon','image')
        params.maxConvexity = cv2.getTrackbarPos('maxCon','image')
         
        # Filter by Inertia
        params.filterByInertia = True
        params.minInertiaRatio = cv2.getTrackbarPos('minIne','image')

        ver = (cv2.__version__).split('.')
        if int(ver[0]) < 3 :
            detector = cv2.SimpleBlobDetector(params)
        else : 
            detector = cv2.SimpleBlobDetector_create(params)
         
        keypoints = detector.detect(im)
        print("detected")
        return keypoints#,im
    @staticmethod
    def printKeypoints(keypoints):
        for keypoint in keypoints:
            pass#print(keypoint.size)
    @staticmethod
    def blobSieve(keypoints):
        keypoints = sorted(keypoints,key=lambda s:s.size)
        if len(keypoints) > 12:
            th = keypoints[len(keypoints)//4].size + 1
            new = []
            for keypoint in keypoints:
                if keypoint.size > th:
                    new.append(keypoint)
            return new
        return keypoints
    
    @staticmethod
    def displayBlobs(image,keypoints,factor,name):
        im_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        height, width = im_with_keypoints.shape[:2]
        cv2.imshow(name,cv2.resize(im_with_keypoints,(int(factor*width), int(factor*height)), interpolation = cv2.INTER_CUBIC))
        print(len(keypoints))
    @staticmethod
    def getKeypoints(name):
        im = 255 - cv2.imread(name, cv2.IMREAD_GRAYSCALE)
        #cv2.imshow("test "+name,im)
        msk = cv2.inRange(im,cv2.getTrackbarPos('minMsk','image'),cv2.getTrackbarPos('maxMsk','image'))
        im = 255 - cv2.bitwise_and(255-im,255-im,mask=msk)
        keypoints = StarDetector.blobSieve(StarDetector.getStarBlobs(im))
        StarDetector.displayBlobs(im,keypoints,1,name)

cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('minThr','image',0,255,nothing)
cv2.createTrackbar('maxThr','image',0,255,nothing)
cv2.createTrackbar('minAre','image',0,6595,nothing)
cv2.createTrackbar('maxAre','image',0,6595,nothing)
cv2.createTrackbar('minCir','image',0,255,nothing)
cv2.createTrackbar('maxCir','image',0,255,nothing)
cv2.createTrackbar('minCon','image',0,255,nothing)
cv2.createTrackbar('maxCon','image',0,255,nothing)
cv2.createTrackbar('minIne','image',0,255,nothing)
cv2.createTrackbar('minMsk','image',0,255,nothing)
cv2.createTrackbar('maxMsk','image',0,255,nothing)

while True:
    StarDetector.getKeypoints("orion.jpg")
    StarDetector.getKeypoints("big_dipper.jpg")
    StarDetector.getKeypoints("leo.jpg")
    cv2.waitKey(1)
quit()
