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


def coefficients(p1, p2):
    a = (p1.y-p2.y) / (p1.x-p2.x)
    return (a, p1.y-a*p1.x)


def functionValue(seg, x):
    a, b = coefficients(seg.start, seg.end)
    return a*x + b


def segmentsIntersect(seg1, seg2):
    s1, e1 = seg1.start, seg1.end
    s2, e2 = seg2.start, seg2.end

    if s1.x == e1.x:
        if min(s1.y, e1.y) <= functionValue(seg2, s1.x) <= max(s1.y, e1.y):
            return True
        return False
    elif s2.x == e2.x:
        if min(s2.y, e2.y) <= functionValue(seg1, s2.x) <= max(s2.y, e2.y):
            return True
        return False

    if (max(s1.x,e1.x) < min(s2.x,e2.x)):
        return False
    a1, b1 = coefficients(s1, e1)
    a2, b2 = coefficients(s2, e2)
    Xa = (b2 - b1) / (a1 - a2)
    return not ((Xa < max( min(s1.x,e1.x), min(s2.x,e2.x) )) or (Xa > min( max(s1.x,e1.x), max(s2.x,e2.x) )))

