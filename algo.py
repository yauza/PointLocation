from typing import List
from utils import *
from structures import *
import random


def createBox(points: List[Point]):
    #left = min(points, key=lambda p : p.x)
    #right = max(points, key=lambda p : p.x)
    #top = max(points, key=lambda p : p.y)
    #bottom = min(points, key=lambda p : p.y)

    #topEdge = Line(Point(left.x, top.y), Point(right.x, top.y))
    #bottomEdge = Line(Point(left.x, bottom.y), Point(right.x, bottom.y))
    left = Point(0,0)
    right = Point(1,0)
    topEdge = Line(Point(0,1), Point(1,1))
    bottomEdge = Line(Point(0,0), Point(1,0))
    return TrapezoidNode(topEdge, bottomEdge, left, right)


def pointLocation(node, point):
    if node.type == "tnode":
        pass
    if node.type == "xnode":
        pass


def findIntersectingTrapezoids(node, segment: Line, intersectingTrapezoids):
    if node.isLeaf:
        if node.containsSegment(segment):
            if node not in intersectingTrapezoids:
                intersectingTrapezoids.append(node)

    elif node.type == 'xnode':
        if segment.start.x >= node.endPoint.x:
            findIntersectingTrapezoids(node.right, segment, intersectingTrapezoids)
        else:
            findIntersectingTrapezoids(node.left, segment, intersectingTrapezoids)
            if segment.end.x >= node.endPoint.x:
                findIntersectingTrapezoids(node.right, segment, intersectingTrapezoids)

    else:
        if node.lineSegment.isPointAbove(segment.start):
            findIntersectingTrapezoids(node.above, segment, intersectingTrapezoids)
        else:
            findIntersectingTrapezoids(node.below, segment, intersectingTrapezoids)


def simpleCase(trNode: TrapezoidNode, edge: Line, dag, visualizer = None):
    old_tr = trNode

    # leftUpperPoint = Point(edge.start.x, functionValue(old_tr.topSegment, edge.start.x))
    # rightUpperPoint = Point(edge.end.x, functionValue(old_tr.topSegment, edge.end.x))
    # leftLowerPoint = Point(edge.start.x, functionValue(old_tr.bottomSegment, edge.start.x))
    # rightLowerPoint = Point(edge.end.x, functionValue(old_tr.bottomSegment, edge.end.x))
    #
    # leftTr = TrapezoidNode()
    # leftTr.topSegment = Line(old_tr.topSegment.start, leftUpperPoint)
    # leftTr.bottomSegment = Line(old_tr.bottomSegment.start, leftLowerPoint)
    # leftTr.leftPoint = old_tr.leftPoint
    # leftTr.rightPoint = edge.end
    #
    # rightTr = TrapezoidNode()
    # rightTr.topSegment = Line(rightUpperPoint, old_tr.topSegment.end)
    # rightTr.bottomSegment = Line(rightLowerPoint, old_tr.bottomSegment.end)
    # rightTr.leftPoint = edge.end
    # rightTr.rightPoint = old_tr.rightPoint
    #
    # topTr = TrapezoidNode()
    # topTr.topSegment = Line(leftUpperPoint, rightUpperPoint)
    # topTr.bottomSegment = edge
    # topTr.leftPoint = edge.start
    # topTr.rightPoint = edge.end
    #
    # bottomTr = TrapezoidNode()
    # bottomTr.topSegment = edge
    # bottomTr.bottomSegment = Line(leftLowerPoint, rightLowerPoint)
    # bottomTr.leftPoint = edge.start
    # bottomTr.rightPoint = edge.end

    # if visualizer is not None:
    #     visualizer.addFigure(topTr.toLines())
    #     visualizer.addFigure(leftTr.toLines())
    #     visualizer.addFigure(rightTr.toLines())
    #     visualizer.addFigure(bottomTr.toLines())

    leftTr = TrapezoidNode(old_tr.topSegment, old_tr.bottomSegment, old_tr.leftPoint, edge.start)
    rightTr = TrapezoidNode(old_tr.topSegment, old_tr.bottomSegment, edge.end, old_tr.rightPoint)
    topTr = TrapezoidNode(old_tr.topSegment, edge, edge.start, edge.end)
    bottomTr = TrapezoidNode(edge, old_tr.bottomSegment, edge.start, edge.end)

    segNode = YNode(edge, topTr, bottomTr)
    v = XNode(edge.end, segNode, rightTr)
    u = XNode(edge.start, leftTr, v)
    trNode.replacePositionWith(dag, u)

    if visualizer is not None:
        visualizer.addDag(dag)


def hardCase(dag: Dag, intersectingTrapezoids, segment: Line, visualizer = None):
    upperMidTrapezoid = None
    lowerMidTrapezoid = None
    mergeUpper = False

    for trapezoid in intersectingTrapezoids:

        if trapezoid.containsPoint(segment.start):
            # case where the left endpoint of the new segment lies in the trapezoid
            leftTrapezoid = TrapezoidNode(trapezoid.topSegment, trapezoid.bottomSegment, trapezoid.leftPoint, segment.start)
            if segment.isPointAbove(trapezoid.rightPoint):
                upperMidTrapezoid = TrapezoidNode(trapezoid.topSegment, segment, segment.start, trapezoid.rightPoint)
                lowerMidTrapezoid = TrapezoidNode(segment, trapezoid.bottomSegment, segment.start, None)
                mergeUpper = False
            else:
                upperMidTrapezoid = TrapezoidNode(trapezoid.topSegment, segment, segment.start, None)
                lowerMidTrapezoid = TrapezoidNode(segment, trapezoid.bottomSegment, segment.start, trapezoid.rightPoint)
                mergeUpper = True

            if segment.start.seen:
                continue

            #if visualizer is not None:
                #visualizer.addFigure(leftTrapezoid.toLines())
               # visualizer.addFigure(upperMidTrapezoid.toLines())
                #visualizer.addFigure(lowerMidTrapezoid.toLines())
            segNode = YNode(segment, upperMidTrapezoid, lowerMidTrapezoid)
            p = XNode(segment.start, leftTrapezoid, segNode)
            trapezoid.replacePositionWith(dag, p)

        elif trapezoid.containsPoint(segment.end):
            # case where the right endpoint of the new segment lies in the trapezoid
            rightTrapezoid = TrapezoidNode(trapezoid.topSegment, trapezoid.bottomSegment, segment.end, trapezoid.rightPoint)
            if mergeUpper:
                upperMidTrapezoid.rightPoint = segment.end
                lowerMidTrapezoid = TrapezoidNode(segment, trapezoid.bottomSegment, trapezoid.leftPoint, segment.end)
            else:
                upperMidTrapezoid = TrapezoidNode(trapezoid.topSegment, segment, trapezoid.leftPoint, segment.end)
                lowerMidTrapezoid.rightPoint = segment.end
            if segment.end.seen:
                continue
            #if visualizer is not None:
               #visualizer.addFigure(rightTrapezoid.toLines())
               # visualizer.addFigure(upperMidTrapezoid.toLines())
                #visualizer.addFigure(lowerMidTrapezoid.toLines())
            segNode = YNode(segment, upperMidTrapezoid, lowerMidTrapezoid)
            q = XNode(segment.end, segNode, rightTrapezoid)
            trapezoid.replacePositionWith(dag, q)

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

           # if visualizer is not None:
               # visualizer.addFigure(upperMidTrapezoid.toLines())
               # visualizer.addFigure(lowerMidTrapezoid.toLines())

            segNode = YNode(segment, upperMidTrapezoid, lowerMidTrapezoid)
            trapezoid.replacePositionWith(dag, segNode)

    if visualizer is not None:
        visualizer.addDag(dag)


#not used
def updateTrapezoidsInConflict(edge: Line, dag):
    leftTrNode = pointLocation(dag.root, edge.start)
    rightTrNode = pointLocation(dag.root, edge.end)
    if leftTrNode == rightTrNode:
        simpleCase(leftTrNode, edge, dag)
    else:
        hardCase()


def algo(edges, visualizer = None):
    points = edgesToPoints(edges)
    # randomized order
    random.shuffle(edges)
    # one-node DAG
    dag = Dag(createBox(points))
    if visualizer is not None:
        #visualizer.addFigure(dag.root.toLines())
        pass

    for edge in edges:
        intersectingTrapezoids = []
        findIntersectingTrapezoids(dag.root, edge, intersectingTrapezoids)
        if len(intersectingTrapezoids) == 1:
            simpleCase(intersectingTrapezoids[0], edge, dag, visualizer)
        else:
            hardCase(dag, intersectingTrapezoids, edge, visualizer)

