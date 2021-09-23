from matplotlib import pyplot as plt
from numpy import array
import os
plt.rcParams['toolbar'] = 'toolmanager'
from matplotlib.backend_tools import ToolBase

if os.path.dirname(__file__) == os.getcwd():
    import Basic
    import Texts
else:
    from . import Basic
    from . import Texts


class showNext(ToolBase):
    """Show next graph."""
    default_keymap = 'N'
    description = 'Show next graph'

    def __init__(self, *args, graph, **kwargs):
        self.graph = graph
        super().__init__(*args, **kwargs)

    def trigger(self, *args, **kwargs):
        self.graph.next()
        self.graph.draw()
        self.graph.mlObj.figure.canvas.draw()

class showPrev(ToolBase):
    """Show next graph."""
    default_keymap = 'P'
    description = 'Show previous graph'

    def __init__(self, *args, graph, **kwargs):
        self.graph = graph
        super().__init__(*args, **kwargs)

    def trigger(self, *args, **kwargs):
        self.graph.prev()
        self.graph.draw()
        self.graph.mlObj.figure.canvas.draw()

        #self.graph.draw(draw=False)




class MatplotlibObject():

    def __init__(self, graph):
        plt.style.use('ggplot')
        #plt.tight_layout()
        self.figure = plt.figure()
        self.figure.canvas.manager.toolmanager.add_tool('Prev', showPrev, graph=graph)
        self.figure.canvas.manager.toolmanager.add_tool('Next', showNext, graph=graph)
        self.figure.canvas.manager.toolbar.add_tool('Prev', 'show')
        self.figure.canvas.manager.toolbar.add_tool('Next', 'show')
        self.ax = self.figure.add_subplot(111)
        self.ax2 = None

    def format(self):
        if self.ax2 is not None:
            self.ax2.grid(None)
        self.ax.grid(True)

    def draw(self):
        plt.show()

    def addYAxis(self):
        self.ax2 = self.ax.twinx()






class Graph():

    def __init__(self, graphSettings, GUIobj, mlObj=None, currIdx=None):
        self.GUIobj = GUIobj
        self.graphSettings = graphSettings

        self.dgObj = None
        if currIdx is None:
            self.currentIdx = 0
        else:
            self.currentIdx = currIdx
        if "y2-axis" in self.graphSettings:
            self.secondYAxis = self.graphSettings["y2-axis"]
        else:
            self.secondYAxis = []
        if "exclude" in self.graphSettings:
            self.exclude = self.graphSettings["exclude"]
        else:
            self.exclude = []
        if mlObj is None:
            self.mlObj = self._getFigure()
        else:
            self.mlObj = mlObj

        if len(self.secondYAxis) > 0:
            self.mlObj.addYAxis()

    def _getFigure(self):
        return MatplotlibObject(self)

    def setLim(self):
        self.setXLim()
        self.setYLim()

    def setXLim(self):
        if "x-lim" in self.graphSettings:
            self.mlObj.ax.set_xlim(self.graphSettings["x-lim"])
            #     self.mlObj.ax.axis(xmin=self.graphSettings["x-lim"][0],
            #                        xmax=self.graphSettings["x-lim"][1])
            # if self.graphSettings["x-lim"][0] is not None:
            #     self.mlObj.ax.axis(xmin=self.graphSettings["x-lim"][0])
            # if self.graphSettings["x-lim"][1] is not None:
            #     self.mlObj.ax.axis(xmax=self.graphSettings["x-lim"][1])

    def setYLim(self):
        if "y2-lim" in self.graphSettings:
            self.mlObj.ax2.set_ylim(self.graphSettings["y2-lim"])
        if "y-lim" in self.graphSettings:
            self.mlObj.ax.set_ylim(self.graphSettings["y-lim"])
        elif "y1-lim" in self.graphSettings:
            self.mlObj.ax.set_ylim(self.graphSettings["y1-lim"])


    def setXLabel(self, label):
        self.mlObj.ax.set_xlabel(label)

    def setYLabels(self, label, label2):
        self.mlObj.ax.set_ylabel(label)
        if self.mlObj.ax2 is not None:
            self.mlObj.ax2.set_ylabel(label2)

    def setTitle(self, title):
        self.mlObj.ax.set_title(title)

    def setCurrIdx(self, idx):
        self.currentIdx = idx

    def next(self):
        self.currentIdx += 1

    def prev(self):
        self.currentIdx -= 1

    def getCurrIdx(self):
        return self.currentIdx

    def setLegend(self, lines, labels):
        self.mlObj.ax.legend(lines, labels, loc='best')






class LineGraph(Graph):

    def __init__(self, graphSettings, GUIobj, mlObj=None, currIdx=None):
        Graph.__init__(self, graphSettings=graphSettings, GUIobj=GUIobj, mlObj=mlObj, currIdx=currIdx)


    def draw(self, dgObj=None, draw=True):

        if dgObj is not None:
            self.dgObj = dgObj
        if self.dgObj is not None:
            if self.dgObj.isDefined():
                xAxis = None
                if "x-axis" in self.graphSettings:
                    xAxisEntity = self.graphSettings["x-axis"]
                    xAxisLabel = xAxisEntity
                    if xAxisEntity in self.dgObj[self.currentIdx]:
                        xAxis = self.dgObj[self.currentIdx][xAxisEntity]
                        xUnits = self.dgObj.getUnits(xAxisEntity)
                        if xUnits is not None:
                            xAxisLabel += ' [' + str(xUnits) + ']'
                    else:
                        self.GUIobj.getError('lineGXNotPres', xAxisEntity, self.dgObj[self.currentIdx].groupDir)
                else:
                    self.GUIobj.getError('lineGXNotSet', self.graphSettings["name"])
                if xAxis is not None:

                    self.mlObj.ax.clear()
                    if self.mlObj.ax2 is not None:
                        self.mlObj.ax2.clear()
                    # TODO move to __init__
                    colors = ["#1abc9c"]
                    lenColors = 1
                    if "colors" in self.graphSettings:
                        if len(self.graphSettings["colors"]) > 0:
                            colors = self.graphSettings["colors"]
                            lenColors = len(colors)
                        else:
                            self.GUIobj.getWarning('graphColEmpty', self.graphSettings["name"])
                    else:
                        self.GUIobj.getWarning('graphColNotSet', self.graphSettings["name"])
                    colIdx = 0
                    yAxisLabel = ''
                    y2AxisLabel = ''
                    comm = ''
                    comm2 = ''
                    lines = []
                    labels = []
                    for entity in self.dgObj[self.currentIdx]:
                        if entity not in self.exclude:
                            if entity is not xAxisEntity:
                                units = self.dgObj.getUnits(entity)
                                if entity in self.secondYAxis:
                                    ax = self.mlObj.ax2
                                    y2AxisLabel += comm2 + entity
                                    if units is not None:
                                        y2AxisLabel += ' [' + str(units) + ']'
                                    comm2 = ', '
                                else:
                                    ax = self.mlObj.ax
                                    yAxisLabel += comm + entity
                                    if units is not None:
                                        yAxisLabel += ' [' + str(units) + ']'
                                    comm = ', '
                                line, = ax.plot(xAxis, self.dgObj[self.currentIdx][entity],
                                               c=colors[colIdx], label=entity) #self.dgObj[self.currentIdx].groupDir
                                lines.append(line)
                                labels.append(entity)
                                colIdx += 1
                                if colIdx >= lenColors:
                                    colIdx = 0
                    self.setXLabel(xAxisLabel)
                    self.setYLabels(yAxisLabel, y2AxisLabel)
                    self.setLegend(lines, labels)
                    self.setLim()
                    self.setTitle(self.dgObj.getFileName(self.currentIdx))
                self.mlObj.format()
                if draw:
                    self.mlObj.draw()
            else:
                if self.mlObj.ax2 is not None:
                    self.mlObj.ax2.clear()
                self.mlObj.ax.clear()
                self.mlObj.format()
                if draw:
                    self.mlObj.draw()





class GraphWrapper():

    types = {"line": LineGraph,
             }

    def __init__(self, graphSettings=None, GUIobj=None, mlObj=None):
        self.graphSettings = graphSettings
        self.mlObj = mlObj
        self.graph = None
        self.dgObj = None
        self.GUIobj = Texts.getTextObj(GUIobj)  # if GUI object is not given (user sets language) use english GUI object
        self.setGraphSettings(graphSettings)

    def setGraphSettings(self, graphSettings):
        gsName = graphSettings
        if graphSettings is not None:
            graphSettings = Basic.loadUserGraphFile(graphSettings, self.GUIobj)
        if graphSettings is None:
            graphSettings = defaultGraphSettings
        if gsName is None:
            graphSettings["name"] = "Default"
        else:
            graphSettings["name"] = gsName
        if self.graph is not None:
            surrIdx = self.graph.getCurrIdx()
        else:
            surrIdx = 0
        if "type" in graphSettings: # TODO add exceptions
            if graphSettings["type"] in self.types:
                self.graph = self.types[graphSettings["type"]](graphSettings, self.GUIobj, self.mlObj, surrIdx)
        else:
            self.graph = self.types[defaultGraphSettings["type"]](defaultGraphSettings, self.GUIobj, self.mlObj,
                                                                  surrIdx)

    def draw(self, dgObj):
        if dgObj is not None:
            self.dgObj = dgObj
            if self.graph is not None:
                self.graph.draw(dgObj)

    def setCurrIdx(self, idx):
        self.graph.setCurrIdx(idx)





defaultGraphSettings = {"type": "line",
                        "colors": ["#000000",  # black
                                   "#e74c3c",  # Alizarin (red)
                                   "#1abc9c",  # Turquoise
                                   "#3498db",  # Peterriver (blue)
                                    "#f1c40f",  # Sunflower (yellow)
                                    "#9b59b6",  # Amethyst (violet)
                                    "#f39c12",  # Orange
                                    "#ecf0f1",  # Clouds (white)
                                    "#2ecc71",  # Emerald
                                    "#2980b9",  # Belizehole (blue)
                                    "#c0392b",  # Pomegranate (red)
                                    "#d35400",  # Pumpkin (orange)
                                   ],
                        "x-axis": "t",
                        }

if __name__ == "__main__":
    from Data import DataGroup
    import Paths
    pdg = DataGroup(Paths.testDir)
    pdg.readPyro('functionalLab')
    g = GraphWrapper('functionalTCGP')
    g.draw(pdg)
