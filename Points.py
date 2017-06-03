import math
import random
import string
import numpy as np
import cv2
import time
import copy


def distance(A,B):
    return math.sqrt(math.pow(A[0] - B[0],2) + math.pow(A[1] - B[1],2))

def rotPot(O,A,d):
    D = math.radians(d)
    sinD = math.sin(D)
    cosD = math.cos(D)
    (x0,y0) = A[0]-O[0],A[1]-O[1]
    x1 = (x0 * cosD) - (y0 * sinD)
    y1 = (y0 * cosD) + (x0 * sinD)
    return x1 + O[0], y1 + O[1]

def fatness(points):
    maxD = -1
    for a in points:
        for b in points:
            maxD = max(maxD,distance(a,b))
    return maxD
def scalify(points):
    fat = fatness(points)
    k = 500.0 / fat
    for point in range(len(points)):
        points[point] = (points[point][0] * k),(points[point][1] * k)
    return points
def boxify(points):
        minX = min(points, key = lambda p: p[0])[0]
        minY = min(points, key = lambda p: p[1])[1]
        for point in range(len(points)):
            points[point] = (points[point][0] - minX),(points[point][1] - minY)
        return points
def closestNeighbour(points,point):
    minD = distance(point,points[0])
    for p in range(1,len(points)):
        minD = min(minD,distance(point,points[p]))
    return minD
def rotEt(points,d):
    for p in range(len(points)):
        points[p] = rotPot((0,0),points[p],d)
    return points
def translate(points,point):
    Xshift = point[0] - points[0][0]
    Yshift = point[1] - points[0][1]
    newPoints = []
    for p in range(len(points)):
        newPoints.append(((points[p][0] + Xshift),(points[p][1] + Yshift)))
    return newPoints

    
def makeShape(points):
    return scalify(boxify(points))

def cp(A,B):
    minimumTest = 10**10
    for point in A:
        translatedShape = translate(B,point)
        minimumRotationalDistance = 10**10
        step = 1
        for a in range(360//step):
            s = 0
            for this in B:
                s += closestNeighbour(A,this)
            minimumRotationalDistance = min(minimumRotationalDistance,s)
        minimumTest = min(minimumTest,minimumRotationalDistance)
    return minimumTest
