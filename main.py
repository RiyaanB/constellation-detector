import cv2
import numpy as np
import time
class StarDetector:
    @staticmethod
    def getStarBlobs(im):
        im = cv2.erode(im,np.ones((2,2)))

        height, width = im.shape[:2]
        area = height * width
        # Setup SimpleBlobDetector parameters.
        params = cv2.SimpleBlobDetector_Params()
         
        # Change thresholds
        params.minThreshold = 4;
        params.maxThreshold = 196;
         
        # Filter by Area.
        params.filterByArea = True
        #10000
        #500
        params.minArea = area/6596.4
        params.maxArea = area/1
         
        # Filter by Circularity
        params.filterByCircularity = True
        params.minCircularity = 0.1
        params.maxCircularity = 1
         
        # Filter by Convexity
        params.filterByConvexity = False
        params.minConvexity = 0.1
        params.maxConvexity = 1
         
        # Filter by Inertia
        params.filterByInertia = True
        params.minInertiaRatio = 0.3

        ver = (cv2.__version__).split('.')
        if int(ver[0]) < 3 :
            detector = cv2.SimpleBlobDetector(params)
        else : 
            detector = cv2.SimpleBlobDetector_create(params)
         
        keypoints = detector.detect(im)
        return keypoints#,im
    @staticmethod
    def printKeypoints(keypoints):
        for keypoint in keypoints:
            print(keypoint.size)
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
        msk = cv2.inRange(im,0,196)
        im = 255 - cv2.bitwise_and(255-im,255-im,mask=msk)
        keypoints = StarDetector.blobSieve(StarDetector.getStarBlobs(im))
        StarDetector.displayBlobs(im,keypoints,1,name)


while True:
    StarDetector.getKeypoints("orion.jpg")
    StarDetector.getKeypoints("big_dipper.jpg")
    StarDetector.getKeypoints("leo.jpg")
    cv2.waitKey(0)
quit()
