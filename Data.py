# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 08:49:06 2021

@author: andmra2
"""

from pandas import DataFrame

import Paths
import IO
import Basic
import Texts
from Functions import ParameterFunctionGroup
#from GUI import GUIfunObj

class Data(object):
    
    def __init__(self, fileName, data=None):
        self.groupDir = fileName
        self.data = data
        self.units = {}
        
    def __set__(self, instance, value):
        self.data = value
        
    def __get__(self, instance, owner):
        return self.data
    
    def __setitem__(self, key, value):
        if key in self.data:
            self.data[key] = value
        if key == 'units':
            self.units = value
        else:
            raise KeyError(key)
        
    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        elif key == 'units':
            return self.units
        else:
            raise KeyError(key)
    
    def __iter__(self):
       return self.data.__iter__()

    def __str__(self):
        return str(self.data)
   
    def rename(self, dic):
        self.data = self.data.rename(columns=dic)

class Parameters(object):

    def __init__(self, groupName='', GUIobj=None):
        self.df = None
        self.GUIobj = Texts.getTextObj(GUIobj)
        self.groupName = groupName
        self.functionFile = None
        self._pfg = ParameterFunctionGroup(Parameter, self.GUIobj.username)

    def __getitem__(self, key):
        if key in self.df.index:
            return self.df.loc[key]
        if key in self.df:
            return self.df[key]
        else:
            raise KeyError(key)

    def __str__(self):
        return str(self.df)

    def setGrpName(self, name):
        self.groupName = name

    def setFunctionFile(self, functionFile):
        self.functionFile = functionFile
        self._pfg.load(self.functionFile)

    def defineFromDict(self, dic):
        self.df = DataFrame.from_dict(dic)


    def getParameters(self, data, functionFile=None):
        if functionFile is not None:
            self.setFunctionFile(functionFile)
        parDict = self._pfg.get(data, grpName=self.groupName)
        if parDict is not None:
            self.defineFromDict(parDict)

    def areDefined(self):
        if self.df is not None:
            return True
        else:
            return False

class Parameter(object):

    def __init__(self, value=None):
        self.value = value
        self.valid = None
        self.units = None
        self.rounding = 2

    def __str__(self):
        valStr = ''
        untStr = ''
        if self.value is not None:
            valStr = str(round(self.value, self.rounding)).replace('.',',')
            if self.units is not None:
                untStr = str(self.units)
        return valStr + untStr

    def __set__(self, instance, value):
        self.value = value

    def __get__(self, instance, owner):
        return self.value

    def setValid(self, valid):
        self.valid = valid

    def isValid(self):
        return self.valid

    def setUnits(self, units):
        self.units = units

    def getUnits(self):
        return self.units

    def setRounding(self, rounding):
        try:
            self.rounding = abs(int(rounding))
        except:
            pass

    def getRounding(self):
        return self.rounding











        

class DataGroup(object):
    
    def __init__(self, groupDir=None, GUIobj=None):
        self.groupDir = groupDir
        # if GUI object is not given (user sets language) use english Text object
        if GUIobj is None:
            self.GUIobj = Texts.getTextObj(GUIobj)
        self._data = {}
        self._units = {}
        self._parameters = Parameters(self.groupDir, self.GUIobj)

    def __set__(self, instance, value):
        self._data = value

    def __get__(self, instance, owner):
        return self._data

    def __setitem__(self, key, value):
        print(key, value)
        self._data[key] = value

    def __getitem__(self, key):
        if key in self._data:
            return self._data[key]
        elif key == 'data':
            return self._data
        elif key == 'parameters':
            return self._parameters
        elif type(key) == int:
            return self.__getitem__(list(self._data.keys())[key])
        else:
            raise KeyError(key)

    def __iter__(self):
        return self._data.__iter__()

    def setFolder(self, folder):
        self.groupDir = folder
        self._parameters.setGrpName(folder)
        
    def dirExists(self):
        return Paths.isdir(self.groupDir)
    
    def listDir(self):
        return Paths.listdir(self.groupDir)
    
    def readPyro(self, headerFile=None):
        if self.dirExists():  # if directory exists 
            for file in self.listDir():  # iterate trough its content
                out = IO.readPyroFile(self.groupDir, file, self.GUIobj)  # try to read every item in the directory
                if out is not None:  # if file as been read 
                    fileName = Basic.removeExt(file)  # get file name without extension
                    self._data[fileName] = Data(fileName, out)  # store file content in a output dictionary
                    #self._data[fileName] = out
                self.GUIobj.moveErrorsToWarnings()
            if headerFile is not None:
                self.transformHeader(headerFile)
        else:  # if directory does not exist return only error
            self.GUIobj.getError('dirNotExists', self.groupDir)
            
    def transformHeader(self, headerFile):
        header = Basic.loadUserHdrFile(headerFile, self.GUIobj)
        if header is not None:
            for parameter in header:
                if "unit" in header[parameter]:
                    self._units[parameter] = header[parameter]["unit"]  # TODO ustvari "unit" objekt
                else:
                    self.GUIobj.getWarning('undfHdrFeatUnt', parameter, headerFile)
                if "headers" in header[parameter]:
                    for file in self._data:
                        for item in self._data[file]:
                            if item.strip() in header[parameter]["headers"]:
                                self._data[file].rename({item: parameter})
                else:
                    self.GUIobj.getWarning('undfHdrFeat', parameter, headerFile)

    def getParameters(self, functionFile=None):
        self._parameters.getParameters(self, functionFile)

    def getUnits(self, parameter):
        if parameter in self._units:
            return self._units[parameter]

    def getFileName(self, idx):
        return list(self._data.keys())[idx]

    def isDefined(self):
        return len(self._data) > 0

    def parametersDefined(self):
        return self._parameters.areDefinded()

            
    
        
        

if __name__ == "__main__":
    pdg = DataGroup(Paths.testDir)
    pdg.readPyro('functionalLab')
    pdg.getParameters('5011-721-414-QC')
    for d in pdg[0]:
        print('line:', d)
