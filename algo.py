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

    return Trapezoid(topEdge, bottomEdge, left, right)


def pointLocation(dag: Node, point):
    if dag.type == "trapezoid":
        return dag
    if dag.type == "point":
        pass


def simpleCase(trNode: Node, edge: Line):
    old_tr = trNode.trapezoid
    leftTr = Trapezoid(Line(old_tr.topE.start, Point(edge.start, old_tr.topE.start.y)), Line(old_tr.bottomE.start, Point(edge.start, old_tr.bottomE.start.y)), old_tr.leftV, edge.end)

    rightTr = Trapezoid(Line(Point(edge.end, old_tr.topE.start.y), old_tr.topE.end), Line(Point(edge.end, old_tr.bottomE.start.y), old_tr.bottomE.end), edge.end, old_tr.rightV)

    topTr = Trapezoid(Line(), edge, edge.start, edge.end)

    bottomTr = Trapezoid(edge, Line(Point(edge.start, old_tr.bottomE), Point()), edge.start, edge.end)


def hardCase():
    pass


def removeTrapezoidsInConflict(edge: Line, dag):
    leftTrNode = pointLocation(dag, edge.start)
    rightTrNode = pointLocation(dag, edge.end)
    if leftTrNode == rightTrNode:
        simpleCase(leftTrNode, edge)
    else:
        hardCase()

def algo(edges):
    points = edgesToPoints(edges)
    box = createBox(points)
    # randomized order
    random.shuffle(edges)
    # one-node DAG
    dag = Node("point",0, points[0])
    for edge in edges:
        removeTrapezoidsInConflict(edge, dag)
