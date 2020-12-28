from ui.lib import *
from .. import utils


class Visualizer:
    def __init__(self, lines = None):
        self.lines = lines
        self.scenes = []
        self.line_color = 'green'
        self.point_color = 'blue'
        if lines is not None:
            self.base_points = utils.edgesToPoints(lines)
            self.addFigure(lines)

    def addFigure(self, lines):
        points = utils.edgesToPoints(lines)
        self.scenes.append(Scene([PointsCollection(points, color=self.point_color)],
                     [LinesCollection(lines, color=self.line_color)]))

    def getScenes(self):
        return self.scenes