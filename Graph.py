from matplotlib import pyplot as plt
from numpy import array

import Basic
import Texts



class MatplotlibObject():

    def __init__(self):
        plt.style.use('ggplot')
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)
        self.ax2 = None

    def format(self):
        if self.ax2 is not None:
            self.ax2.grid(None)
        self.ax.grid(True)

    def draw(self):
        print('here')
        plt.show()

    def addYAxis(self):
        self.ax2 = self.ax.twinx()





class Graph():

    def __init__(self, graphSettings, GUIobj, mlObj=None):
        self.GUIobj = GUIobj
        self.graphSettings = graphSettings
        self.secondYAxis = []
        if "y2-axis" in self.graphSettings:
            self.secondYAxis = self.graphSettings["y2-axis"]
        if mlObj is None:
            self.mlObj = self._getFigure()
        else:
            self.mlObj = mlObj
        if len(self.secondYAxis) > 0:
            self.mlObj.addYAxis()

    def _getFigure(self):
        return MatplotlibObject()

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






class LineGraph(Graph):

    def __init__(self, graphSettings, GUIobj, mlObj=None):
        Graph.__init__(self, graphSettings=graphSettings, GUIobj=GUIobj, mlObj=mlObj)
        self.currentIdx = 0

    def draw(self, dgObj):

        xAxis = None
        if "x-axis" in self.graphSettings:
            xAxisEntity = self.graphSettings["x-axis"]
            xAxisLabel = xAxisEntity
            if xAxisEntity in dgObj[self.currentIdx]:
                xAxis = dgObj[self.currentIdx][xAxisEntity]
                xUnits = dgObj.getUnits(xAxisEntity)
                if xUnits is not None:
                    xAxisLabel += ' [' + str(xUnits) + ']'
            else:
                self.GUIobj.getError('lineGXNotPres', xAxisEntity, dgObj[self.currentIdx].groupDir)
        else:
            self.GUIobj.getError('lineGXNotSet', self.graphSettings["name"])
        if xAxis is not None:

            self.mlObj.ax.clear()
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
            for entity in dgObj[self.currentIdx]:
                if entity is not xAxisEntity:
                    units = dgObj.getUnits(entity)
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
                    ax.plot(xAxis, dgObj[self.currentIdx][entity],
                            c=colors[colIdx], label=dgObj[self.currentIdx].groupDir)
                    colIdx += 1
                    if colIdx >= lenColors:
                        colIdx = 0
            self.setXLabel(xAxisLabel)
            self.setYLabels(yAxisLabel, y2AxisLabel)
            self.setLim()
            self.setTitle(dgObj.getFileName(self.currentIdx))
            self.mlObj.format()
            self.mlObj.draw()






class GraphWrapper():

    types = {"line": LineGraph,
             }

    def __init__(self, graphSettings=None, GUIobj=None, mlObj=None):
        self.graphSettings = graphSettings
        self.mlObj = mlObj
        gsName = graphSettings
        self.GUIobj = Texts.getTextObj(GUIobj)  # if GUI object is not given (user sets language) use english GUI object
        if graphSettings is not None:
            graphSettings = Basic.loadUserGraphFile(graphSettings, self.GUIobj)
        if graphSettings is None:
            graphSettings = defaultGraphSettings
        if gsName is None:
            graphSettings["name"] = "Default"
        else:
            graphSettings["name"] = gsName
        if "type" in graphSettings: # TODO add exceptions
            if graphSettings["type"] in self.types:
                self.graph = self.types[graphSettings["type"]](graphSettings, self.GUIobj, self.mlObj)
        else:
            self.graph = self.types[defaultGraphSettings["type"]](defaultGraphSettings, self.GUIobj, self.mlObj)

    def draw(self, dgObj):
        self.graph.draw(dgObj)




defaultGraphSettings = {"type": "line",
                        "colors": ["#1abc9c", # Turquoise
                                   "#3498db", # Peterriver (blue)
                                    "#e74c3c", # Alizarin (red)
                                    "#f1c40f", # Sunflower (yellow)
                                    "#9b59b6", # Amethyst (violet)
                                    "#f39c12",  # Orange
                                    "#ecf0f1",  # Clouds (white)
                                    "#2ecc71", # Emerald
                                    "#2980b9" # Belizehole (blue)
                                    "#c0392b", # Pomegranate (red)
                                    "#d35400",  # Pumpkin (orange)
                                   ],
                        "x-axis": "t",
                        }

if __name__ == "__main__":
    from Data import DataGroup
    import Paths
    pdg = DataGroup(Paths.testDir)
    pdg.readPyro('functionalLab')
    g = GraphWrapper('functionalGP')
    g.draw(pdg)
