class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __gt__(self, other):
        if self.x > other.x:
            return True
        return False


class Node:
    def __init__(self, type, index, point1 = None, point2 = None):
        self.type = type
        self.point1 = point1
        self.point2 = point2
        self.index = index
        self.trapezoid = None
        self.leftNode = None
        self.rightNode = None


class Line:
    def __init__(self, start, end):
        if start < end:
            self.start = start
            self.end = end
        else:
            self.start = end
            self.end = start


class Trapezoid:
    def __init__(self, topE, bottomE, leftV, rightV):
        self.topE = topE
        self.bottomE = bottomE
        self.leftV = leftV
        self.rightV = rightV

        self.upperRight = None
        self.upperLeft = None
        self.lowerLeft = None
        self.lowerRight = None

    # def __eq__(self):


