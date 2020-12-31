from ui.lib import *
from utils import *


class DagData:
    def __init__(self):
        self.lines = []
        self.points = []
        self.trapezoids = []


class Visualizer:
    def __init__(self, lines):
        self.lines = lines
        self.scenes = []
        self.line_color = 'green'
        self.point_color = 'blue'
        self.trapezoid_color = 'darkblue'
        if lines is not None:
            self.base_points = edgesToUIPoints(lines)
            self.addFigure(lines)

    def addFigure(self, lines):
        points = uiEdgesToUIPoints(lines)
        self.lines.extend(lines)
        self.scenes.append(Scene([PointsCollection(points, color=self.point_color)],
                     [LinesCollection(self.lines, color=self.line_color)]))

    def addDag(self, dag):
        dagData = DagData()
        self.traverseDag(dagData, dag.root)
        trLines = []
        for trapezoid in dagData.trapezoids:
            trLines.extend(trapezoid)
        self.scenes.append(Scene([PointsCollection(dagData.points, color=self.point_color)],
                     [LinesCollection(trLines, color=self.trapezoid_color),
                      LinesCollection(dagData.lines, color=self.line_color)]))

    def addDagWithResult(self, dag, tr, point):
        dagData = DagData()
        self.traverseDag(dagData, dag.root)
        trLines = []
        for trapezoid in dagData.trapezoids:
            trLines.extend(trapezoid)
        self.scenes.append(Scene([PointsCollection(dagData.points, color=self.point_color),
                                  PointsCollection([point.toList()], color='red')],
                                 [LinesCollection(trLines, color=self.trapezoid_color),
                                  LinesCollection(dagData.lines, color=self.line_color),
                                  LinesCollection(tr.getDrawable(), color='magenta')]))

    def traverseDag(self, dagData: DagData, node):
        if node is None:
            return
        if node.type == "tnode":
            dagData.trapezoids.append(node.getDrawable())
            return
        elif node.type == "xnode":
            dagData.points.append(node.endPoint.toList())
            self.traverseDag(dagData, node.left)
            self.traverseDag(dagData, node.right)
        else:
            dagData.lines.append(node.lineSegment.toList())
            self.traverseDag(dagData, node.above)
            self.traverseDag(dagData, node.below)

    def getScenes(self):
        return self.scenes