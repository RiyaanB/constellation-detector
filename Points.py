import math
import random
import string
import numpy as np
import cv2
import time


orion = Points([(203.99999999999997, 79.73193560922681), (201.99888306503846, 508.97151815848036), (135.96202421130712, 265.8358105606514), (112.94917945924924, 161.77772994265058), (111.94862099176846, 173.7844315524199), (108.94694558932612, 194.7961593695162), (104.94471171940303, 281.84474604034386), (74.92795769497971, 300.8553569224786), (64.92237302017196, 560.0), (8.891098841248407, 466.9480625242877), (-16.122862845771067, 83.73416947914993)])
class Points:

    @staticmethod
    def distance(A,B):
        return math.sqrt(math.pow(A[0] - B[0],2) + math.pow(A[1] - B[1],2))
    @staticmethod
    def comparePoint(A,B):
        # True, False
        if A[0] > B[0]:
            return True
        elif A[0] < B[0]:
            return False
        else:
            return (True if A[1] > B[1] else False)

    @staticmethod
    def rotate(O,A,d):
        D = math.radians(d)
        (x0,y0) = A[0]-O[0],A[1]-O[1]
        sinD = math.sin(D)
        cosD = math.cos(D)
        x1 = (x0 * cosD) - (y0 * sinD)
        y1 = (y0 * cosD) + (x0 * sinD)
        return x1 + O[0], y1 + O[1]

    def __init__(self,pointList):
        for point in range(len(pointList)):
            pointList[point] = int(pointList[point][0] + 0.5),int(pointList[point][1] + 0.5)
        self.pointList = pointList
        self.sort()
        self.boxify()
        self.maxDistance()
        self.scalify()
        
    def maxDistance(self):
        maxD = -1
        for a in self.pointSort:
            for b in self.pointSort:
                if maxD < Points.distance(a,b):
                    maxD = Points.distance(a,b)
                    A = a
                    B = b
        self.fat = int(maxD)
        return A,B

    def sort(self):
        self.pointSort = []
        while len(self.pointList) != 0:
            ma = (-1,-1)
            ma_index = -1
            for point in range(len(self.pointList)):
                if Points.comparePoint(self.pointList[point],ma):
                    ma = self.pointList[point]
                    ma_index = point
            self.pointSort.insert(0,ma)
            self.pointList.pop(ma_index)
        self.pointList.reverse()
    def boxify(self):
        minX = min(self.pointSort, key = lambda p: p[0])[0]
        minY = min(self.pointSort, key = lambda p: p[1])[1]
        for a in range(len(self.pointSort)):
            self.pointSort[a] = (self.pointSort[a][0] - minX),(self.pointSort[a][1] - minY)
    def width(self):
        minX = min(self.pointSort, key = lambda p: p[0])[0]
        maxX = max(self.pointSort, key = lambda p: p[0])[0]
        return maxX - minX
    def height(self):
        minY = min(self.pointSort, key = lambda p: p[1])[1]
        maxY = max(self.pointSort, key = lambda p: p[1])[1]
        return maxY - minY
    def mean(self):
        sumX = 0
        sumY = 0
        for point in self.pointSort:
            sumX += point[0]
            sumY += point[1]
        return sumX//len(self.pointSort),sumY//len(self.pointSort)
    def __str__(self):
        return self.pointSort
    def display(self):
        t = time.clock()
        #1 2 3 4 5 6 8 9 10 12 15
        step = 3
        c = 360//step
        for a in range(c):
            blank_image = np.zeros((1000,1000,3),np.uint8)
            self.rotateEntire(step)
            mean = self.mean()
            for point in self.pointSort:
                blank_image[int(point[1]-mean[1]+500)][int(point[0]-mean[0]+500)] = [255,255,255]
            cv2.imshow("Lol",blank_image)
            cv2.waitKey(1)
        print(time.clock() - t)
    def scalify(self):
        self.oldPointSort = self.pointSort
        A,B = self.maxDistance()
        self.k = 500.0 / math.sqrt(math.pow(A[0]-B[0],2)+math.pow(A[1]-B[1],2))
        for point in range(len(self.pointSort)):
            self.pointSort[point] = self.pointSort[point][0] * self.k,self.pointSort[point][1] * self.k
        self.boxify()
    def rotateEntire(self,d):
        mean = self.mean()
        for point in range(len(self.pointSort)):
            self.pointSort[point] = Points.rotate((mean[0],mean[1]),self.pointSort[point],d)
            
def comparePoints(A,B):
    A.scalify()
    B.scalify()

    #A is preloaded
    for point in A.pointSort:
        
