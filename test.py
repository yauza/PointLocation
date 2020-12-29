from ui.lib import Plot
from ui.plot_utils import getLineSegments
from ui.visualizer import Visualizer


def coefficients(p1, p2):
    a = (p1.y-p2.y) / (p1.x-p2.x)
    return (a, p1.y-a*p1.x)


def functionValue(seg, x):
    a, b = coefficients(seg.leftPoint, seg.rightPoint)
    return a*x + b


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


def updateMapForOneTrapezoid(tzMap, trapezoid, segment, visualizer = None):
    leftTrapezoid = TrapezoidNode(trapezoid.topSegment, trapezoid.bottomSegment, trapezoid.leftPoint, segment.leftPoint)
    topTrapezoid = TrapezoidNode(trapezoid.topSegment, segment, segment.leftPoint, segment.rightPoint)
    bottomTrapezoid = TrapezoidNode(segment, trapezoid.bottomSegment, segment.leftPoint, segment.rightPoint)
    rightTrapezoid = TrapezoidNode(trapezoid.topSegment, trapezoid.bottomSegment, segment.rightPoint, trapezoid.rightPoint)

    segNode = YNode(segment, topTrapezoid, bottomTrapezoid)
    q = XNode(segment.rightPoint, segNode, rightTrapezoid)
    p = XNode(segment.leftPoint, leftTrapezoid, q)
    trapezoid.replacePositionWith(tzMap, p)

    if visualizer is not None:
        visualizer.addDag(tzMap)


def updateMapForManyTrapezoids(tzMap, intersectingTrapezoids, segment, visualizer):

    upperMidTrapezoid = None
    lowerMidTrapezoid = None
    mergeUpper = False

    for trapezoid in intersectingTrapezoids:

        if trapezoid.containsPoint(segment.leftPoint):
            # case where the left endpoint of the new segment lies in the trapezoid
            leftTrapezoid = TrapezoidNode(trapezoid.topSegment, trapezoid.bottomSegment, trapezoid.leftPoint, segment.leftPoint)
            if segment.isPointAbove(trapezoid.rightPoint):
                upperMidTrapezoid = TrapezoidNode(trapezoid.topSegment, segment, segment.leftPoint, trapezoid.rightPoint)
                lowerMidTrapezoid = TrapezoidNode(segment, trapezoid.bottomSegment, segment.leftPoint, None)
                mergeUpper = False
            else:
                upperMidTrapezoid = TrapezoidNode(trapezoid.topSegment, segment, segment.leftPoint, None)
                lowerMidTrapezoid = TrapezoidNode(segment, trapezoid.bottomSegment, segment.leftPoint, trapezoid.rightPoint)
                mergeUpper = True

            if segment.leftPoint.seen:
                continue
            segNode = YNode(segment, upperMidTrapezoid, lowerMidTrapezoid)
            p = XNode(segment.leftPoint, leftTrapezoid, segNode)
            trapezoid.replacePositionWith(tzMap, p)

        elif trapezoid.containsPoint(segment.rightPoint):
            # case where the right endpoint of the new segment lies in the trapezoid
            rightTrapezoid = TrapezoidNode(trapezoid.topSegment, trapezoid.bottomSegment, segment.rightPoint, trapezoid.rightPoint)
            if mergeUpper:
                upperMidTrapezoid.rightPoint = segment.rightPoint
                lowerMidTrapezoid = TrapezoidNode(segment, trapezoid.bottomSegment, trapezoid.leftPoint, segment.rightPoint)
            else:
                upperMidTrapezoid = TrapezoidNode(trapezoid.topSegment, segment, trapezoid.leftPoint, segment.rightPoint)
                lowerMidTrapezoid.rightPoint = segment.rightPoint
            if segment.rightPoint.seen:
                continue
            segNode = YNode(segment, upperMidTrapezoid, lowerMidTrapezoid)
            q = XNode(segment.rightPoint, segNode, rightTrapezoid)
            trapezoid.replacePositionWith(tzMap, q)

        else:
            # case where the no endpoint of the new segment lies in the trapezoid
            if mergeUpper:
                lowerMidTrapezoid = TrapezoidNode(segment, trapezoid.bottomSegment, trapezoid.leftPoint, None)
            else:
                upperMidTrapezoid = TrapezoidNode(trapezoid.topSegment, segment, trapezoid.leftPoint, None)

            if segment.isPointAbove(trapezoid.rightPoint):
                upperMidTrapezoid.rightPoint = trapezoid.rightPoint
                mergeUpper = False
            else:
                lowerMidTrapezoid.rightPoint = trapezoid.rightPoint
                mergeUpper = True

            segNode = YNode(segment, upperMidTrapezoid, lowerMidTrapezoid)
            trapezoid.replacePositionWith(tzMap, segNode)

    if visualizer is not None:
        visualizer.addDag(tzMap)


def findIntersectingTrapezoids1(node, segment, intersectingTrapezoids):
    if node.isLeaf:
        if node.containsSegment(segment):
            if node not in intersectingTrapezoids:
                intersectingTrapezoids.append(node)

    elif node.type == 'xnode':
        if segment.leftPoint.x >= node.endPoint.x:
            findIntersectingTrapezoids1(node.right, segment, intersectingTrapezoids)
        else:
            findIntersectingTrapezoids1(node.left, segment, intersectingTrapezoids)
            if segment.rightPoint.x >= node.endPoint.x:
                findIntersectingTrapezoids1(node.right, segment, intersectingTrapezoids)

    else:
        ##if node.lineSegment.isPointAbove(segment.leftPoint):
        findIntersectingTrapezoids1(node.above, segment, intersectingTrapezoids)
        ##else:
        findIntersectingTrapezoids1(node.below, segment, intersectingTrapezoids)


class TZMap:
    def __init__(self, root):
        self.root = root

    def updateRoot(self, root):
        self.root = root


def createBox():
    left = Point("",0,0)
    right = Point("",1,0)
    topEdge = Segment("",Point("",0,1), Point("",1,1))
    bottomEdge = Segment("",Point("",0,0), Point("",1,0))
    return TrapezoidNode(topEdge, bottomEdge, left, right)


def alg(lineSegments, visualizer = None):
    tzMap = TZMap(createBox())

    for segment in lineSegments:
        intersectingTrapezoids = []
        findIntersectingTrapezoids1(tzMap.root, segment, intersectingTrapezoids)
        print(len(intersectingTrapezoids))
        # handle new segment in two cases: it either intersects one trapezoid or many of them
        if len(intersectingTrapezoids) == 1:
            updateMapForOneTrapezoid(tzMap, intersectingTrapezoids[0], segment, visualizer)
        else:
            updateMapForManyTrapezoids(tzMap, intersectingTrapezoids, segment, visualizer)


def getLineObjects(lines):
    return [Segment("",Point("",line[0][0], line[0][1]), Point("",line[1][0], line[1][1])) for line in lines]


def test():
    visualizer = Visualizer([])
    plot = Plot()
    plot.draw()

    lines = getLineObjects(getLineSegments(plot))

    alg(lines, visualizer)

    plot = Plot(visualizer.getScenes())
    plot.draw()


test()