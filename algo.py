from typing import List
from utils import *
from structures import *
import random


def createBox(points: List[Point]):
    left = min(points, key=lambda p : p.x)
    right = max(points, key=lambda p : p.x)
    top = max(points, key=lambda p : p.y)
    bottom = min(points, key=lambda p : p.y)

    topEdge = Line(Point(left.x, top.y), Point(right.x, top.y))
    bottomEdge = Line(Point(left.x, bottom.y), Point(right.x, bottom.y))

    return TrapezoidNode(topEdge, bottomEdge, left, right)


def pointLocation(node, point):
    if node.type == "tnode":
        pass
    if node.type == "xnode":
        pass


def findIntersectingTrapezoids(node, segment, intersectingTrapezoids):
    if node.isLeaf:
        if node.containsSegment(segment):
            if node not in intersectingTrapezoids:
                intersectingTrapezoids.append(node)

    elif node.type == 'xnode':
        if segment.leftPoint.x >= node.endPoint.x:
            findIntersectingTrapezoids(node.right, segment, intersectingTrapezoids)
        else:
            findIntersectingTrapezoids(node.left, segment, intersectingTrapezoids)
            if segment.rightPoint.x >= node.endPoint.x:
                findIntersectingTrapezoids(node.right, segment, intersectingTrapezoids)

    else:
        if node.lineSegment.isPointAbove(segment.leftPoint):
            findIntersectingTrapezoids(node.above, segment, intersectingTrapezoids)
        else:
            findIntersectingTrapezoids(node.below, segment, intersectingTrapezoids)


def simpleCase(trNode, edge: Line, dag):
    old_tr = trNode.trapezoid

    leftUpperPoint = Point(edge.start, functionValue(old_tr.topE, edge.start))
    rightUpperPoint = Point(edge.end, functionValue(old_tr.topE, edge.end))
    leftLowerPoint = Point(edge.start, functionValue(old_tr.bottomE, edge.start))
    rightLowerPoint = Point(edge.end, functionValue(old_tr.bottomE, edge.end))

    leftTr = TrapezoidNode()
    leftTr.topE = Line(old_tr.topE.start, leftUpperPoint)
    leftTr.bottomE = Line(old_tr.bottomE.start, leftLowerPoint)
    leftTr.leftV = old_tr.leftV
    leftTr.rightV = edge.end

    rightTr = TrapezoidNode()
    rightTr.topE = Line(rightUpperPoint, old_tr.topE.end)
    rightTr.bottomE = Line(rightLowerPoint, old_tr.bottomE.end)
    rightTr.leftV = edge.end
    rightTr.rightV = old_tr.rightV

    topTr = TrapezoidNode()
    topTr.topE = Line(leftUpperPoint, rightUpperPoint)
    topTr.bottomE = edge
    topTr.leftV = edge.start
    topTr.rightV = edge.end

    bottomTr = TrapezoidNode()
    bottomTr.topE = edge
    bottomTr.bottomE = Line(leftLowerPoint, rightLowerPoint)
    bottomTr.leftV = edge.start
    bottomTr.rightV = edge.end

    segNode = YNode(edge, topTr, bottomTr)
    v = XNode(edge.end, segNode, rightTr)
    u = XNode(edge.start, leftTr, v)
    trNode.replacePositionWith(dag, u)



def hardCase():
    pass


def removeTrapezoidsInConflict(edge: Line, dag):
    leftTrNode = pointLocation(dag, edge.start)
    rightTrNode = pointLocation(dag, edge.end)
    if leftTrNode == rightTrNode:
        simpleCase(leftTrNode, edge, dag)
    else:
        hardCase()


def algo(edges):
    points = edgesToPoints(edges)
    # randomized order
    random.shuffle(edges)
    # one-node DAG
    dag = Dag(createBox(points))

    for edge in edges:
        removeTrapezoidsInConflict(edge, dag)
