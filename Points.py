import math

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
    def __init__(self,pointList):
        for point in range(len(pointList)):
            pointList[point] = int(pointList[point][0] + 0.5),int(pointList[point][1] + 0.5)
        self.pointList = pointList
        self.sort()

    def maxDistance(self):
        maxD = -1
        for a in self.pointSort:
            for b in self.pointSort:
                maxD = max(Points.distance(a,b),maxD)
        self.fat = maxD

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
    def __str__(self):
        return self.pointSort
