
def edgesToPoints(edges):
    points = []
    for e in edges:
        points.append(e.start)
        points.append(e.end)

    return points