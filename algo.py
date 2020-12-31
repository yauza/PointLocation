from ui.lib import Plot
from ui.plot_utils import getLineSegments
from ui.visualizer import Visualizer
import random
from structures import *

"""
    Segment intersects only one
    trapezoid.
"""


def simpleCase(tzMap, trapezoid, segment, visualizer = None):
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


"""
    Segment intersects multiple
    trapezoids.
"""


def hardCase(tzMap, intersectedTrapezoids, segment, visualizer):

    upperMidTrapezoid = None
    lowerMidTrapezoid = None
    mergeUpper = False

    for trapezoid in intersectedTrapezoids:

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


def findIntersectedTrapezoids(node, segment, intersectedTrapezoids):
    if node.isLeaf:
        if node.containsSegment(segment):
            if node not in intersectedTrapezoids:
                intersectedTrapezoids.append(node)

    elif node.type == 'xnode':
        if segment.leftPoint.x >= node.endPoint.x:
            findIntersectedTrapezoids(node.right, segment, intersectedTrapezoids)
        else:
            findIntersectedTrapezoids(node.left, segment, intersectedTrapezoids)
            if segment.rightPoint.x >= node.endPoint.x:
                findIntersectedTrapezoids(node.right, segment, intersectedTrapezoids)

    else:
        ##if node.lineSegment.isPointAbove(segment.leftPoint):
        findIntersectedTrapezoids(node.above, segment, intersectedTrapezoids)
        ##else:
        findIntersectedTrapezoids(node.below, segment, intersectedTrapezoids)


class Dag:
    def __init__(self, root):
        self.root = root

    def updateRoot(self, root):
        self.root = root


def createBoundingBox():
    left = Point("",0,0)
    right = Point("",1,0)
    topEdge = Segment("",Point("",0,1), Point("",1,1))
    bottomEdge = Segment("",Point("",0,0), Point("",1,0))
    return TrapezoidNode(topEdge, bottomEdge, left, right)


def findArea(node, point):
    if node.isLeaf:
        if node.containsPoint(point):
            return node
        else:
            return None
    elif node.type == 'xnode':
        if point.x >= node.endPoint.x:
            return findArea(node.right, point)
        else:
            return findArea(node.left, point)
    else:
        tr1 = findArea(node.above, point)
        if tr1 is not None:
            return tr1
        tr2 = findArea(node.below, point)
        return tr2


def algo(lineSegments, visualizer = None):
    dag = Dag(createBoundingBox())

    # random.shuffle(lineSegments)
    for l in lineSegments:
        print(l)
    for segment in lineSegments:
        intersectedTrapezoids = []
        findIntersectedTrapezoids(dag.root, segment, intersectedTrapezoids)
        print(len(intersectedTrapezoids))
        # handle new segment in two cases: it either intersects one trapezoid or many of them
        if len(intersectedTrapezoids) == 1:
            simpleCase(dag, intersectedTrapezoids[0], segment, visualizer)
        else:
            hardCase(dag, intersectedTrapezoids, segment, visualizer)

    test_point1 = Point("", 0.5, 0.5)
    test_point2 = Point('', 0.3, 0.7)
    tr1 = findArea(dag.root, test_point1)
    tr2 = findArea(dag.root, test_point2)
    if visualizer is not None:
        visualizer.addDagWithResult(dag, tr1, test_point1)
        visualizer.addDagWithResult(dag, tr2, test_point2)

    return dag




