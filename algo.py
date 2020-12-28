from typing import List
from utils import *
from structures import *
import random


def createBox(points: List[Point]):
    left = min(points, key=lambda p : p.x)
    right = max(points, key=lambda p : p.x)
    top = max(points, key=lambda p : p.y)
    bottom = min(points, key=lambda p : p.y)

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

    leftUpperPoint = Point(edge.start.x, functionValue(old_tr.topSegment, edge.start.x))
    rightUpperPoint = Point(edge.end.x, functionValue(old_tr.topSegment, edge.end.x))
    leftLowerPoint = Point(edge.start.x, functionValue(old_tr.bottomSegment, edge.start.x))
    rightLowerPoint = Point(edge.end.x, functionValue(old_tr.bottomSegment, edge.end.x))

    leftTr = TrapezoidNode()
    leftTr.topSegment = Line(old_tr.topSegment.start, leftUpperPoint)
    leftTr.bottomSegment = Line(old_tr.bottomSegment.start, leftLowerPoint)
    leftTr.leftPoint = old_tr.leftPoint
    leftTr.rightPoint = edge.end

    rightTr = TrapezoidNode()
    rightTr.topSegment = Line(rightUpperPoint, old_tr.topSegment.end)
    rightTr.bottomSegment = Line(rightLowerPoint, old_tr.bottomSegment.end)
    rightTr.leftPoint = edge.end
    rightTr.rightPoint = old_tr.rightPoint

    topTr = TrapezoidNode()
    topTr.topSegment = Line(leftUpperPoint, rightUpperPoint)
    topTr.bottomSegment = edge
    topTr.leftPoint = edge.start
    topTr.rightPoint = edge.end

    bottomTr = TrapezoidNode()
    bottomTr.topSegment = edge
    bottomTr.bottomSegment = Line(leftLowerPoint, rightLowerPoint)
    bottomTr.leftPoint = edge.start
    bottomTr.rightPoint = edge.end

    if visualizer is not None:
        visualizer.addFigure(topTr.toLines())
        visualizer.addFigure(leftTr.toLines())
        visualizer.addFigure(rightTr.toLines())
        visualizer.addFigure(bottomTr.toLines())

    segNode = YNode(edge, topTr, bottomTr)
    v = XNode(edge.end, segNode, rightTr)
    u = XNode(edge.start, leftTr, v)
    trNode.replacePositionWith(dag, u)



def hardCase():
    pass


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
        simpleCase(intersectingTrapezoids[0], edge, dag, visualizer)
        # updateTrapezoidsInConflict(edge, dag)

