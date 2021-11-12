import os
if os.path.dirname(__file__) == os.getcwd():
    from Functions import ParameterFunctionGroup, SeriesFunctionGroup
else:
    from .Functions import ParameterFunctionGroup, SeriesFunctionGroup

def getParameterFunctions(GUIobj):
    return list(ParameterFunctionGroup.functionTypes.keys())

def getSeriesFunctions(GUIobj):
    return list(SeriesFunctionGroup.functionTypes.keys())

def getMandatorySett(ftype, functionName):
    if ftype == "p":
        return ParameterFunctionGroup.functionTypes[functionName].mandatorySett
    elif ftype == "s":
        return SeriesFunctionGroup.functionTypes[functionName].mandatorySett
