from openpyxl.styles import Font, Fill, PatternFill, NamedStyle, Border, Side
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.drawing.image import Image


import Paths
import Graph

class ExcelWorkbook(Workbook):

    def __init__(self):
        Workbook.__init__(self)
        self._sheets = [ExcelWorksheet(self, "Sheet1")]

    def create_sheet(self, title=None, index=None):
        if title is None:
            title = "Sheet{}".format(len(self.worksheets)+1)
        self._sheets.append(ExcelWorksheet(self, title))

    def setSheetTitle(self, title):
        self.active.title = title

    def adBlock(self, block):
        self.active.addBlock(block)

    def save(self, filename, *args, **kwargs):
        for worksheet in self.worksheets:
            worksheet.insert(*args, **kwargs)
        self.active = 0
        super().save(filename)

class ExcelWorksheet(Worksheet):

    def __init__(self, parent, title):
        Worksheet.__init__(self, parent, title)
        self.blocks = []

    def addBlock(self, block):
        self.blocks.append(block)

    def insert(self, *args, **kwargs):
        kwargs["worksheet"] = self
        kwargs["occupied"] = [0, 0]
        for block in self.blocks:
            kwargs["occupied"] = block.insert(*args, **kwargs)





class ExcelBlock(object):

    badVal = NamedStyle(name="bad")
    goodVal = NamedStyle(name="good")
    badVal.fill = PatternFill("solid", fgColor="ff8585")
    goodVal.fill = PatternFill("solid", fgColor="7beded")
    bd = Side(style='thin', color="000000")
    badVal.border = Border(left=bd, top=bd, right=bd, bottom=bd)
    goodVal.border = Border(left=bd, top=bd, right=bd, bottom=bd)
    numberFormats = ['0', '0.0', '0.00', '0.000', '0.0000']

    def __init__(self, position=None, direction=0):
        self.direction = direction
        if position is None:
            self.relPosition = [0, 0]
            self.position = [0, 0]
        else:
            self.definePosition(position)
        #self.worksheet = None

    def definePosition(self, position):
        self.relPosition = position
        self.position = position


    def getPosition(self, *args, **kwargs):
        if "worksheet" in kwargs:
            self.worksheet = kwargs["worksheet"]
        else:
            return False
        if "occupied" in kwargs:
            if self.direction:
                self.position[0] = kwargs["occupied"][0] + self.relPosition[0]
                self.position[1] = self.relPosition[1]
            else:
                self.position[0] = self.relPosition[0]
                self.position[1] = kwargs["occupied"][1] + self.relPosition[1]
        return True

    def getOccupied(self, endPosition, **kwargs):
        if "occupied" in kwargs:
            if self.direction:
                return [kwargs["occupied"][0] + endPosition[0],
                        max(kwargs["occupied"][1], endPosition[1])]
            else:
                return [endPosition[0],
                        kwargs["occupied"][1] + endPosition[1]]

    def getAnchor(self, column, row):
        leftOver = column+1
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        charsLen = len(chars)
        anchor = str(row+1)
        while leftOver > 0:
            mod = leftOver % charsLen
            char = chars[mod-1]
            leftOver = int((leftOver - mod)/charsLen)
            anchor = char + anchor
        return anchor



class ExcelPictureList(ExcelBlock):

    def __init__(self):
        self.path = None
        self.dataGroup = 0

    def setPath(self, path):
        self.path = path

    def setDataGroup(self, dg):
        self.dataGroup = dg


class ExcelParameterTable(ExcelBlock):

    def __init__(self, position=None, direction=0):
        self.dataGroup = 0
        ExcelBlock.__init__(self, position, direction)

    def setDataGroup(self, dg):
        self.dataGroup = dg

    def insert(self, *args, **kwargs):
        if self.getPosition(*args, **kwargs) and "groups" in kwargs:
            dataGroup = kwargs["groups"][self.dataGroup]
            parameters = dataGroup["parameters"]
            self.worksheet.merge_cells(start_row=self.position[1]+1,
                                       start_column=self.position[0]+1,
                                       end_row=self.position[1]+1,
                                       end_column=self.position[0]+len(parameters)+1)
            cell = self.worksheet.cell(row=self.position[1] + 1,
                                       column=self.position[0] + 1)
            cell.value = parameters.groupName
            for row, index in enumerate(parameters.df.index):
                cell = self.worksheet.cell(row=self.position[1]+row+3,
                                           column=self.position[0]+1)
                cell.value = str(index)
                if True:# evaluate: TODO
                    if parameters.areValid(index):
                        cell.style = self.goodVal
                    else:
                        cell.style = self.badVal
            for i, entity in enumerate(parameters):
                col = self.position[0] + i + 2
                cell = self.worksheet.cell(row=self.position[1]+2,
                                           column=col)
                cell.value = entity
                for j, dPoint in enumerate(parameters[entity]):
                    cell = self.worksheet.cell(row=self.position[1]+j+3,
                                               column=col)
                    cell.value = dPoint.value
                    if True: # evaluate: TODO
                        if parameters[j][i].isValid():
                            style = self.goodVal.__copy__()
                        else:
                            style = self.badVal.__copy__()
                    style.number_format = self.numberFormats[dPoint.rounding]
                    cell.style = style
            return self.getOccupied([col, self.position[1]+j+3], **kwargs)
        return self.getOccupied([0, 0], **kwargs)


class ExcelGraphList(ExcelBlock):
    graphSize = (19.20, 7.6)

    def __init__(self, graphFile, position=None, direction=0):
        self.setGraphFile(graphFile)
        self.dataGroup = 0
        ExcelBlock.__init__(self, position, direction)

    def setGraphFile(self, graphFile):
        self._gw = Graph.GraphWrapper(graphFile)

    def setDataGroup(self, dg):
        self.dataGroup = dg

    def getGraphs(self, *args, **kwargs):
        graphs = []
        if "groups" in kwargs:
            dg = kwargs["groups"][self.dataGroup]
            cont = True
            graphs.append(self._gw.graph.draw(dg, draw=False, size=self.graphSize))
            while cont:
                cont = self._gw.graph.next()
                graphs.append(self._gw.graph.draw(dg, draw=False, size=self.graphSize))
        return graphs


    def insert(self, *args, **kwargs):
        if self.getPosition(*args, **kwargs) and "groups" in kwargs:
            if "listDown" in kwargs:
                listDown= kwargs["listDirection"]
            else:
                listDown = False
            graphs = self.getGraphs(*args, **kwargs)
            for i, graph in enumerate(graphs):
                img = Image(graph)
                img.anchor = self.getAnchor(self.position[0]+i*30*(not listDown),
                                            self.position[1]+i*38*listDown)
                self.worksheet.add_image(img)
            return self.getOccupied([self.position[0]+i*30*(not listDown)+30,
                                     self.position[1]+i*38*listDown+38], **kwargs)
        return self.getOccupied([0, 0], **kwargs)








if __name__ == "__main__":
    from Data import DataGroup

    wb = ExcelWorkbook()
    wb.setSheetTitle("Parametri")
    #wb.adBlock(ExcelParameterTable([2, 3]))

    # wb.create_sheet("Grafi")
    # wb.active = 1
    wb.adBlock(ExcelGraphList('functionalGP', [2, 3], 0))
    wb.adBlock(ExcelParameterTable([1, 1], 0))
    # wb.adBlock(ExcelParameterTable([2, 3], 0))


    data = DataGroup()
    data.setFolder(Paths.testDir)
    data.readPyro('functionalLab')
    # sfg = SeriesFunctionGroup()
    # sfg.load('5011-721-414')
    # sfg.apply(data)
    data.getParameters('5011-721-414-QC')

    wb.save("test.xlsx", groups=[data])
    # eg = ExcelGraph('functionalGP', [2, 3], 0)
    # print(eg.getAnchor(27, 5))


