from utils import functionValue, coefficients
# from algo import *

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.seen = False

    def toList(self):
        return [self.x, self.y]


class Line:
    def __init__(self, start, end):
        if start.x < end.x:
            self.start = start
            self.end = end
        else:
            self.start = end
            self.end = start
        if start.x != end.x:
            self.a, self.b = coefficients(self.start, self.end)

    def isPointAbove(self, point):
        if point.y > (self.a * point.x) + self.b:
            return True
        return False

    def toList(self):
        return [(self.start.x, self.start.y), (self.end.x, self.end.y)]


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

    def containsSegment(self, segment: Line):
        if self.containsPoint(segment.start) or self.containsPoint(segment.end):
            return True
        resY = functionValue(segment, self.leftPoint.x)
        if resY is not None:
            leftIntersection = Point(self.leftPoint.x, resY)
            if self.containsPoint(leftIntersection):
                return True
        return False

    def containsPoint(self, point):
        if self.leftPoint.x <= point.x <= self.rightPoint.x:
            return self.bottomSegment.isPointAbove(point) and not self.topSegment.isPointAbove(point)
        return False

    def replacePositionWith(self, dag, node):
        if not self.parents:
            dag.setRoot(node)
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

    def toLines(self):
        lines = [self.topSegment.toList(), self.bottomSegment.toList()]
        leftVerticalLine = Line(self.topSegment.start, self.bottomSegment.start)
        if self.rightPoint is not None:
            rightVerticalLine = Line(self.topSegment.end, self.bottomSegment.end)
            lines.append(rightVerticalLine.toList())
        lines.append(leftVerticalLine.toList())
        return lines

    def getDrawable(self):
        newTr = createTrapezoid(self.topSegment, self.bottomSegment, self.leftPoint, self.rightPoint)
        return newTr.toLines()


class Dag:
    def __init__(self, root):
        self.setRoot(root)

    def setRoot(self, root):
        self.root = root


def createTrapezoid(topSegment, bottomSegment, leftPoint, rightPoint):
    newTr = TrapezoidNode()

    leftUpperPoint = Point(leftPoint.x, functionValue(topSegment, leftPoint.x))
    leftLowerPoint = Point(leftPoint.x, functionValue(bottomSegment, leftPoint.x))
    rightUpperPoint = Point(rightPoint.x, functionValue(topSegment, rightPoint.x))
    rightLowerPoint = Point(rightPoint.x, functionValue(bottomSegment, rightPoint.x))

    newTr.topSegment = Line(leftUpperPoint, rightUpperPoint)
    newTr.bottomSegment = Line(leftLowerPoint, rightLowerPoint)
    newTr.leftPoint = leftPoint
    newTr.rightPoint = rightPoint

    return newTr