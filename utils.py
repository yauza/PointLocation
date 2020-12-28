from structures import Line
from typing import List


def edgesToPoints(edges):
    points = []
    for e in edges:
        points.append(e.start)
        points.append(e.end)

    return points

def edgesToUIPoints(edges: List[Line]):
    points = []
    for e in edges:
        points.append([e.start.x, e.start.y])
        points.append([e.end.x, e.end.y])

    return points

def edgesToUILines(edges: List[Line]):
    lines = []
    for e in edges:
        lines.append([[e.start.x, e.start.y], [e.end.x, e.end.y]])

    return lines