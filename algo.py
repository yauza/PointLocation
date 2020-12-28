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




def pointLocation(dag, point):
    pass


def removeTrapezoidsInConflict(edge: Line, dag):
    leftTrapezoid = pointLocation(dag, edge.start)


def algo(edges):
    points = edgesToPoints(edges)
    box = createBox(points)
    # randomized order
    random.shuffle(edges)
    # one-node DAG
    dag = Node("point",0, points[0])
    for edge in edges:
        removeTrapezoidsInConflict(edge, dag)
