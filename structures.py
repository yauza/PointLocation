from utils import functionValue
# from algo import *


class Point:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.seen = False

    def toList(self):
        return [self.x, self.y]

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) +  ")"


class Segment:
    def __init__(self, name, p, q):
        self.name = name
        self.leftPoint = p
        self.rightPoint = q
        if q.x < p.x:
            self.leftPoint = q
            self.rightPoint = p

        if p.x != q.x:
            self.slope = (self.rightPoint.y - self.leftPoint.y) / (self.rightPoint.x - self.leftPoint.x)
            self.const = self.leftPoint.y - (self.slope * self.leftPoint.x)

    def isPointAbove(self, point):
        if point.y > (self.slope * point.x) + self.const:
            return True
        return False

    def getY(self, x):
        if self.leftPoint.x <= x <= self.rightPoint.x:
            return (self.slope * x) + self.const
        return None

    def toList(self):
        return [(self.leftPoint.x, self.leftPoint.y), (self.rightPoint.x, self.rightPoint.y)]

    def __str__(self):
        return str(self.leftPoint) + ", " + str(self.rightPoint)


class XNode:
    def __init__(self, point, left=None, right=None):
        self.isLeaf = False
        self.type = 'xnode'
        self.setLeft(left)
        self.setRight(right)
        self.endPoint = point
        self.endPoint.seen = True

    def setLeft(self, node):
        self.left = node
        if node is None:
            return
        if node.isLeaf and self not in node.parents:
            node.parents.append(self)

    def setRight(self, node):
        self.right = node
        if node is None:
            return
        if node.isLeaf and self not in node.parents:
            node.parents.append(self)

    def getName(self):
        return self.endPoint.name


class YNode:
    def __init__(self, segment, above=None, below=None):
        self.isLeaf = False
        self.type = 'ynode'
        self.setAbove(above)
        self.setBelow(below)
        self.lineSegment = segment

    def setAbove(self, node):
        self.above = node
        if node is None:
            return
        if node.isLeaf and self not in node.parents:
            node.parents.append(self)

    def setBelow(self, node):
        self.below = node
        if node is None:
            return
        if node.isLeaf and self not in node.parents:
            node.parents.append(self)

    def getName(self):
        return self.lineSegment.name


class TrapezoidNode:
    def __init__(self, topSegment = None, bottomSegment = None, leftPoint = None, rightPoint = None):
        self.isLeaf = True
        self.type = 'tnode'
        self.topSegment = topSegment
        self.bottomSegment = bottomSegment
        self.leftPoint = leftPoint
        self.rightPoint = rightPoint
        self.parents = []
        self.name = None

    def containsSegment(self, segment):
        if self.containsPoint(segment.leftPoint) or self.containsPoint(segment.rightPoint):
            return True
        resY = segment.getY(self.leftPoint.x)
        if resY is not None:
            leftIntersection = Point(None, self.leftPoint.x, resY)
            if self.containsPoint(leftIntersection):
                return True
        return False

    def containsPoint(self, point):
        if self.leftPoint.x <= point.x <= self.rightPoint.x:
            return self.bottomSegment.isPointAbove(point) and not self.topSegment.isPointAbove(point)
        return False

    def replacePositionWith(self, tzMap, node):
        if not self.parents:
            tzMap.updateRoot(node)
            return
        for parent in self.parents:
            if parent.type == 'xnode':
                if parent.left == self:
                    parent.setLeft(node)
                else:
                    parent.setRight(node)
            else:
                if parent.above == self:
                    parent.setAbove(node)
                else:
                    parent.setBelow(node)

    def getName(self):
        return self.name

    def toLines(self):
        lines = [self.topSegment.toList(), self.bottomSegment.toList()]
        leftVerticalLine = Segment("",self.topSegment.leftPoint, self.bottomSegment.leftPoint)
        if self.rightPoint is not None:
            rightVerticalLine = Segment("",self.topSegment.rightPoint, self.bottomSegment.rightPoint)
            lines.append(rightVerticalLine.toList())
        lines.append(leftVerticalLine.toList())
        return lines

    def getDrawable(self):
        newTr = createTrapezoid(self.topSegment, self.bottomSegment, self.leftPoint, self.rightPoint)
        return newTr.toLines()


def createTrapezoid(topSegment, bottomSegment, leftPoint, rightPoint):
    newTr = TrapezoidNode()

    leftUpperPoint = Point("",leftPoint.x, functionValue(topSegment, leftPoint.x))
    leftLowerPoint = Point("",leftPoint.x, functionValue(bottomSegment, leftPoint.x))
    rightUpperPoint = Point("",rightPoint.x, functionValue(topSegment, rightPoint.x))
    rightLowerPoint = Point("",rightPoint.x, functionValue(bottomSegment, rightPoint.x))

    newTr.topSegment = Segment("",leftUpperPoint, rightUpperPoint)
    newTr.bottomSegment = Segment("",leftLowerPoint, rightLowerPoint)
    newTr.leftPoint = leftPoint
    newTr.rightPoint = rightPoint

    return newTr
