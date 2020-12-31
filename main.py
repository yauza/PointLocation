from algo import algo, findArea
from ui.lib import Plot
from ui.visualizer import Visualizer
from ui.plot_utils import *
from polygons import pol1, pol1_toLines, pol2, pol2_toLines, pol2_alal


if __name__ == '__main__':
    visualizer = Visualizer([])
    # plot = Plot()
    # plot.draw()
    #
    # lines = getLineObjects(getLineSegments(plot))
    #lines = generateRandomLineSegments(1000, 0, 1000, 0, 1000)
    #dag = algo(lines, visualizer)
    dag = algo(pol2_alal, visualizer)

    # tr = findArea(dag.root,Point("",0.5,0.5))
    # visualizer.addFigure(tr.toLines())
    # visualizer.addFigure(pol2_toLines)
    plot = Plot(visualizer.getScenes())
    plot.draw()


