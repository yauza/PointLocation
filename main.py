from algo import algo
from structures import Line, Point
from ui.lib import Plot
from ui.visualizer import Visualizer
from ui.plot_utils import *


if __name__ == '__main__':
    visualizer = Visualizer([])
    plot = Plot()
    plot.draw()

    lines = getLineObjects(getLineSegments(plot))
    #lines = generateRandomLineSegments(1000, 0, 1000, 0, 1000)

    algo(lines, visualizer)

    plot = Plot(visualizer.getScenes())
    plot.draw()



