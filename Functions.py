# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 12:30:07 2021

@author: andmra2
"""

from numpy import where
import os

if os.path.dirname(__file__) == os.getcwd():
    import Basic
    import Paths
    import Texts
else:
    from . import Paths
    from . import Basic
    from . import Texts


class ParameterFunction(object):
    
    def __init__(self, fun, ParameterObj=None, GUIobj=None):
        self.GUIobj = Texts.getTextObj(GUIobj)
        self.ParameterObj = ParameterObj
        funParam = fun['parameters']
        if 'feature1' in funParam:  # if feature1 is defined in funParam set its value to self.feature1
            self.feature1 = funParam['feature1']
        else:  # if feature1 is not defined in funParam set self.feature1 value to None
            self.feature1 = None
        if 'feature2' in funParam:  # if feature2 is defined in funParam set its value to self.feature2
            self.feature2 = funParam['feature2']
        else:  # if feature2 is not defined in funParam set self.feature2 value to None
            self.feature2 = None
        if 'value' in funParam:  # if value is defined in funParam set its value to self.value
            self.value = funParam['value']
        else:  # if value is not defined in funParam set self.value value to None
            self.value = None
        if 'evaluation' in fun:  # if evaluation is defined in funParam create Evaluation object from the definition
            self.evaluation = Evaluation(fun['evaluation'], GUIobj=self.GUIobj)
        else:  # else create empty Evaluation object
            self.evaluation = Evaluation()
        if 'rounding' in funParam:  # if rounding is defined in funParam
            if type(funParam['rounding']) == int:  # if rounding type is integer set the value from funParam
                self.rounding = funParam['rounding']  
            else:  
                try:  # if rounding type is not integer try to convert funParam value to integer type
                    self.rounding = int(funParam['rounding'])
                except:  # if conversion fails set roundding value to None
                    self.rounding = None
        else:  # if rounding is not defined set it as None
            self.rounding = None

    def groupGet(self, groupPd, evaluate=True, parameter=''):
        output = {}  # initialize output dictionary
        for fileName in groupPd:  # iterate trough file names in groupPd
            output[fileName] = self.get(groupPd, evaluate, fileName, parameter)  # get function values for given file
            self.GUIobj.moveErrorsToWarnings()  # if error occurs append it to warnings
        return output  # return output

    def getParameter(self, value, evaluate, units):
        parameter = self.ParameterObj(value)
        parameter.setRounding(self.rounding)
        parameter.setUnits(units)
        if evaluate:  # if evaluation is wanted evaluate function value
            parameter.setValid(self.evaluation.validate(parameter))
        return parameter

        
        
        
class Evaluation(object):
    
    def __init__(self, evalPar={}, GUIobj=None):
        self.GUIobj = Texts.getTextObj(GUIobj)
        if 'max' in evalPar:  # if max is defined in evalPar set its value to self.max
            self.max = evalPar['max']
        else:  # if max is not defined in evalPar set self.max as None
            self.max = None
        if 'min' in evalPar:  # if min is defined in evalPar set its value to self.min
            self.min = evalPar['min']
        else:  # if min is not defined in evalPar set self.min as None
            self.min = None

            
    def validate(self, value):  # evaluate if function value is in range [self.min, self.max]
        if value is not None:  # if value is defined evaluate it
            if self.max is not None:  # if self.max is defined check if value is less or equal
                if value > self.max:
                    return False  # if value is higher than self.max return False
            if self.min is not None:  # if self.min is defined check if value is more or equal
                if value < self.min:
                    return False  # if value is lower than self.min return False
            return True  # if value is in specified range return True
        return False  # if value is not defined (None) return False
                    
    
    
class MaxParFunction(ParameterFunction):
    
    def __init__(self, funParam, ParameterObj=None, GUIobj=None):
        ParameterFunction.__init__(self, funParam, ParameterObj, GUIobj)

    def get(self, data, evaluate=True, fileName='', parameter=''):
        output = self.ParameterObj()#{'value': None, 'valid': None}  # initialize output dictionary
        pd = data[fileName]
        if pd is not None:
            if self.feature1 in pd:  # if feature exists in pd store its max value
                units = data.getUnits(self.feature1)
                output = self.getParameter(pd[self.feature1].max(), evaluate, units)
                return output
            else:   # if feature does not exist in pd return featrNotExist warning
                self.GUIobj.getWarning('featrNotExist', self.feature1, fileName)
                return output
        self.GUIobj.getError('fileNotParamet', self.feature1, fileName)
        return output


class MinParFunction(ParameterFunction):

    def __init__(self, funParam, ParameterObj=None, GUIobj=None):
        ParameterFunction.__init__(self, funParam, ParameterObj, GUIobj)

    def get(self, data, evaluate=True, fileName='', parameter=''):
        output = self.ParameterObj()#{'value': None, 'valid': None}  # initialize output dictionary
        pd = data[fileName]
        if pd is not None:
            if self.feature1 in pd:  # if feature exists in pd store its min value
                units = data.getUnits(self.feature1)
                output = self.getParameter(pd[self.feature1].min(), evaluate, units)
                return output
            else:  # if feature does not exist in pd return featrNotExist warning
                self.GUIobj.getWarning('featrNotExist', self.feature1, fileName)
                return output
        self.GUIobj.getError('fileNotParamet', self.feature1, fileName)
        return output

class AtParFunction(ParameterFunction):

    def __init__(self, funParam, ParameterObj=None, GUIobj=None):
        ParameterFunction.__init__(self, funParam, ParameterObj, GUIobj)

    def get(self, data, evaluate=True, fileName='', parameter=''):
        output = self.ParameterObj()#{'value': None, 'valid': None}  # initialize output dictionary
        pd = data[fileName]
        if pd is not None:
            if self.feature2 in pd:  # if feature1 exists in pd
                if self.value is not None:  # if value is defined get index of its first occurrence in pd
                    valueIdx = where(pd[self.feature2] >= self.value)[0]  # TODO implement also for falling values and warning for not numerical values
                    if len(valueIdx) > 0:  # if value reaches threshold
                        valueIdx = valueIdx[0]  # get its first occurrence
                        if self.feature1 in pd:  # if feature1 exists in pd
                            if len(pd[self.feature1]) > valueIdx:  # if valueIdx exists in feature1 get its value
                                units = data.getUnits(self.feature1)
                                output = self.getParameter(pd[self.feature1][valueIdx], evaluate, units)
                            else:  #
                                self.GUIobj.getWarning('idxAtInv', self.feature1, self.feature2, self.value, fileName)
                        else:
                            self.GUIobj.getWarning('featrNotExist', self.feature1, fileName)
                    else:
                        self.GUIobj.getWarning('valNotReached', self.feature2, self.value, fileName)
                else:
                    self.GUIobj.getWarning('tarValNotSet', self.feature2, parameter)
                return output
            else:  # if feature does not exist in pd return featrNotExist warning
                self.GUIobj.getWarning('featrNotExist', self.feature2, fileName)
                return output
        self.GUIobj.getError('fileNotParamet', self.feature1, fileName)
        return output

class ParameterFunctionGroup(object):
    
    functionTypes = {'max': MaxParFunction,
                     'min': MinParFunction,
                     'at': AtParFunction,
                     }
    
    def __init__(self, ParameterObj=None, GUIobj=None):
        self.functions = {}
        self.ParameterObj = ParameterObj
        self.GUIobj = Texts.getTextObj(GUIobj)  # if GUI object is not given (user sets language) use english GUI object
        self.functionFile = None
        #self.username = username
        
    def load(self, functionFile):
        self.functionFile = functionFile
        parFun = Basic.loadUserParFunFile(self.functionFile, self.GUIobj)
        if parFun is not None:
            return self.parseFunctions(parFun)
#        if self.username is not None:
#            userParFunFile = Paths.getUserParFunFile(self.username, functionFile)
#            if Paths.isfile(userParFunFile):
#                parFun = Basic.loadJsonFile(userParFunFile)
#                out, warnings, errors = self.parseFunctions(parFun, textObj)
#                return out, warnings, errors
#        globalParFunFile = Paths.getGlobalParFunFile(functionFile)
#        if Paths.isfile(globalParFunFile):
#            parFun = Basic.loadJsonFile(globalParFunFile)
#            out, warnings, errors = self.parseFunctions(parFun, textObj)
#            return out, warnings, errors
        
    def parseFunctions(self, parFun):
        for parameter in parFun:
            if 'function' in parFun[parameter]:
                functionType = parFun[parameter]['function']
                if functionType in self.functionTypes:
                    self.functions[parameter] = self.functionTypes[functionType](parFun[parameter],
                                                                                 self.ParameterObj,
                                                                                 self.GUIobj)
                else:
                    self.GUIobj.getWarning('unknParFunType', functionType, parameter)
            else:
                self.GUIobj.getWarning('undfParFunType', parameter)
    
    def get(self, groupPd, evaluate=True, grpName=''):
        output = {}
        if groupPd is not None:
            for parameter in self.functions:
                output[parameter] = self.functions[parameter].groupGet(groupPd, evaluate, parameter)
            return output
        else:
            self.GUIobj.getError('grpNotParamet', grpName)
            return output



class SeriesFunction(object):

    def __init__(self, fun, GUIobj=None):
        self.GUIobj = Texts.getTextObj(GUIobj)
        funSeries = fun['series']
        if 'feature1' in funSeries:  # if feature1 is defined in funSeries set its value to self.feature1
            self.feature1 = funSeries['feature1']
        else:  # if feature1 is not defined in funSeries set self.feature1 value to None
            self.feature1 = None
        if 'feature2' in funSeries:  # if feature2 is defined in funSeries set its value to self.feature2
            self.feature2 = funSeries['feature2']
        else:  # if feature2 is not defined in funSeries set self.feature2 value to None
            self.feature2 = None
        if 'value' in funSeries:  # if value is defined in funSeries set its value to self.value
            self.value = funSeries['value']
        else:  # if value is not defined in funSeries set self.value value to None
            self.value = None
        # if 'evaluation' in fun:  # if evaluation is defined in funSeries create Evaluation object from the definition
        #     self.evaluation = Evaluation(fun['evaluation'], GUIobj=self.GUIobj)
        # else:  # else create empty Evaluation object
        #     self.evaluation = Evaluation()
        # if 'rounding' in funSeries:  # if rounding is defined in funSeries
        #     if type(funSeries['rounding']) == int:  # if rounding type is integer set the value from funSeries
        #         self.rounding = funSeries['rounding']
        #     else:
        #         try:  # if rounding type is not integer try to convert funSeries value to integer type
        #             self.rounding = int(funSeries['rounding'])
        #         except:  # if conversion fails set roundding value to None
        #             self.rounding = None
        # else:  # if rounding is not defined set it as None
        #     self.rounding = None

    def groupApply(self, groupPd, parameter=''):
        for fileName in groupPd:  # iterate trough file names in groupPd
            self.apply(groupPd, fileName, parameter)  # get function values for given file
            self.GUIobj.moveErrorsToWarnings()  # if error occurs append it to warnings

    # def getParameter(self, value, evaluate, units):
    #     parameter = self.SeriesObj(value)
    #     parameter.setRounding(self.rounding)
    #     parameter.setUnits(units)
    #     if evaluate:  # if evaluation is wanted evaluate function value
    #         parameter.setValid(self.evaluation.validate(parameter))
    #     return parameter


class ShiftFunction(SeriesFunction):

    def __init__(self, funSer, GUIobj=None):
        SeriesFunction.__init__(self, funSer, GUIobj)

    def apply(self, data, fileName='', functionName=''):
        #output = self.SeriesObj()  # {'value': None, 'valid': None}  # initialize output dictionary
        pd = data[fileName]
        if pd is not None:
            if self.feature1 in pd:  # if feature exists in pd continue
                #units = data.getUnits(self.feature1)
                if self.value is not None:  # if value for the shift is defined continue
                    if Basic.isNumerical(self.value):  # if value for the shift is numerical shift feature
                        pd[self.feature1] += self.value
                    else:  # if value for the shift is not numerical raise warning
                        self.GUIobj.getWarning('funValNotNum', self.feature1, functionName, self.value)
                else:    # if value for the shift is not defined raise warning
                    self.GUIobj.getWarning('funValNotSet', self.feature1, functionName)
            else:  # if feature does not exist in pd return featrNotExist warning
                self.GUIobj.getWarning('featrNotExist', self.feature1, fileName)
        else:
            self.GUIobj.getError('fileNotShift', self.feature1, fileName)



class SeriesFunctionGroup(object):

    functionTypes = {"shift": ShiftFunction,
                     }

    def __init__(self, GUIobj=None):
        self.functions = {}
        self.GUIobj = Texts.getTextObj(GUIobj)  # if GUI object is not given (user sets language) use english GUI object
        self.functionFile = None
        # self.username = username

    def load(self, functionFile):
        self.functionFile = functionFile
        parFun = Basic.loadUserSerFunFile(self.functionFile, self.GUIobj)
        if parFun is not None:
            return self.parseFunctions(parFun)

    #        if self.username is not None:
    #            userParFunFile = Paths.getUserParFunFile(self.username, functionFile)
    #            if Paths.isfile(userParFunFile):
    #                parFun = Basic.loadJsonFile(userParFunFile)
    #                out, warnings, errors = self.parseFunctions(parFun, textObj)
    #                return out, warnings, errors
    #        globalParFunFile = Paths.getGlobalParFunFile(functionFile)
    #        if Paths.isfile(globalParFunFile):
    #            parFun = Basic.loadJsonFile(globalParFunFile)
    #            out, warnings, errors = self.parseFunctions(parFun, textObj)
    #            return out, warnings, errors

    def parseFunctions(self, parFun):
        for sFunction in parFun:
            if 'function' in parFun[sFunction]:
                functionType = parFun[sFunction]['function']
                if functionType in self.functionTypes:
                    self.functions[sFunction] = self.functionTypes[functionType](parFun[sFunction],
                                                                                 self.GUIobj)
                else:
                    self.GUIobj.getWarning('unknSerFunType', functionType, sFunction)
            else:
                self.GUIobj.getWarning('undfSerFunType', sFunction)

    def apply(self, groupPd, grpName=''):
        output = {}
        if groupPd is not None:
            for sFunction in self.functions:
                output[sFunction] = self.functions[sFunction].groupApply(groupPd, sFunction)
            return output
        else:
            self.GUIobj.getError('grpNotSeries', grpName)
            return output


                    
                

if __name__ == "__main__":
    from Data import DataGroup
    data = DataGroup()
    data.setFolder(Paths.testDir)
    data.readPyro('functionalLab')
    sfg = SeriesFunctionGroup()
    sfg.load('5011-721-414')
    sfg.apply(data)
    data.getParameters('5011-721-414-QC')

    print(data._parameters)
#    funPar = Basic.loadJsonFile(Paths.getGlobalParFunFile('5011-721-414-QC'))
#    maxFun = MaxParFunction(funPar['Tmax'])
#    par, war, err = maxFun.groupGet(out)

