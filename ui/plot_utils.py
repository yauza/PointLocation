from random import randint

from structures import Line, Point


def getLineSegments(plot):
    segments = plot.get_added_elements().lines[0].lines
    return segments

def getLineObjects(lines):
    return [Line(Point(line[0][0], line[0][1]), Point(line[1][0], line[1][1])) for line in lines]


def getPoints(plot):
    seg = plot.get_added_elements().lines[0].lines
    points = []

    for l in seg:
        points.append(l[0])
        points.append(l[1])

    return points


def generateRandomLineSegments(n, min_x, max_x, min_y, max_y):
    segments = []
    s = set()

    while n > 0:
        x1 = randint(min_x, max_x)
        x2 = randint(min_x, max_x)

        y1 = randint(min_y, max_y)
        y2 = randint(min_y, max_y)

        if x1 == x2:
            continue

        if x1 in s or x2 in s:
            continue

        if x1 > x2:
            segments.append(((x2, y2), (x1, y1)))
        else:
            segments.append(((x1, y1), (x2, y2)))

        s.add(x1)
        s.add(x2)
        n -= 1

    return segments