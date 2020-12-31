from typing import List


def edgesToPoints(edges):
    points = []
    for e in edges:
        points.append(e.leftPoint)
        points.append(e.rightPoint)

    return points


def edgesToUIPoints(edges):
    points = []
    for e in edges:
        points.append([e.start.x, e.start.y])
        points.append([e.end.x, e.end.y])

    return points


def edgesToUILines(edges):
    lines = []
    for e in edges:
        lines.append([[e.start.x, e.start.y], [e.end.x, e.end.y]])
    return lines


def uiEdgesToUIPoints(lines):
    points = []
    for line in lines:
        points.extend(line)
    return points


def coefficients(p1, p2):
    a = (p1.y-p2.y) / (p1.x-p2.x)
    return (a, p1.y-a*p1.x)


def functionValue(seg, x):
    a, b = coefficients(seg.leftPoint, seg.rightPoint)
    return a*x + b


def functionValueWithCheck(seg, x):
    a, b = coefficients(seg.leftPoint, seg.rightPoint)
    val = a*x + b
    if min(seg.leftPoint.y, seg.rightPoint.y) <= val <= max(seg.rightPoint.y, seg.leftPoint.y):
        return val
    else:
        return seg.rightPoint.y