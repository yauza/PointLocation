from structures import Line, Point
from ui.lib import Plot
from ui.visualizer import Visualizer

if __name__ == '__main__':
    line1 = Line(Point(1,1), Point(2,2))
    visualizer = Visualizer([line1])
    plot = Plot(visualizer.getScenes())
    plot.draw()


