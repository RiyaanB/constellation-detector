import cv2
import numpy as np
import math
import time

class StarMap:
    def __init__(self,name,display=True):
        self.name = name
        self.basicRaw = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
        self.getAllKeypoints()
        self.getSievedKeypoints()
        if display:
            self.display()
    def getAllKeypoints(self):
        self.rawInverse = 255 - self.basicRaw.copy()
        msk = cv2.inRange(self.rawInverse,0,165)
        self.basicRawMasked = 255 - cv2.bitwise_and(self.basicRaw,self.basicRaw,mask=msk)
        im = cv2.erode(self.basicRawMasked,np.ones((1,3)))

        height, width = im.shape[:2]
        area = height * width
        
        params = cv2.SimpleBlobDetector_Params()
         
        params.minThreshold = 4;
        params.maxThreshold = 255;
         
        params.filterByArea = True
        
        params.minArea = area/6590
        params.maxArea = area/711
         
        params.filterByCircularity = True
        params.minCircularity = 0
        params.maxCircularity = 255
         
        params.filterByConvexity = False
        params.minConvexity = 0
        params.maxConvexity = 255
         
        params.filterByInertia = True
        params.minInertiaRatio = 0

        ver = (cv2.__version__).split('.')
        if int(ver[0]) < 3 :
            detector = cv2.SimpleBlobDetector(params)
        else : 
            detector = cv2.SimpleBlobDetector_create(params)
         
        self.keypoints = detector.detect(im)
    def getSievedKeypoints(self):
        keypoints = sorted(self.keypoints,key=lambda s:s.size)
        if len(keypoints) > 12:
            th = keypoints[len(keypoints)//4].size + 1
            new = []
            for keypoint in keypoints:
                if keypoint.size > th:
                    new.append(keypoint)
            self.sievedKeypoints = new
        self.sievedKeypoints = self.keypoints
        print(len(self.sievedKeypoints))
    def display(self):
        self.withKeypoints = cv2.drawKeypoints(self.rawInverse, self.sievedKeypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        height, width = self.withKeypoints.shape[:2]
        factor = 1
        cv2.imshow(self.name,cv2.resize(self.withKeypoints,(int(factor*width), int(factor*height)), interpolation = cv2.INTER_CUBIC))

StarMap('orion.jpg')
StarMap('big_dipper.jpg')
StarMap('leo.jpg')
while True:
    cv2.waitKey(1)
