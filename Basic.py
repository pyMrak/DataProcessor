# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 10:20:23 2021

@author: andmra2
"""
import json
import os
import re
import shutil
from numpy import argsort, array
import numbers

if os.path.dirname(__file__) == os.getcwd():
    import Paths
else:
    from . import Paths





# loads json file
def loadJsonFile(fileName, textObj=None):
    with open(fileName) as jsonFile:
        try:
            return json.load(jsonFile)
        except:
            if textObj is not None:
                textObj.getError('jsonNotReadable', fileName)
            else:
                print('jsonNotReadable', fileName)  # TODO popravi na bolj "GUI" varianto
            return {}

def saveJsonFile(fileName, content, textObj=None):
    with open(fileName, "w") as jsonFile:
        return json.dump(content, jsonFile, indent=4)


# checks if file is a txt file
def isTxt(file):
    return file[-4:] == '.txt'


# removes extension from the file name
def removeExt(file):
    return file.split('.',1)[0]


# joins directory path with file name
def joinFilePath(dirPath, file):
    return '/'.join((dirPath, file))


def loadServerFile(serverFile, userLocFun, globalLocFun, err, textObj=None):
    if textObj is not None:
        if textObj.username is not None:
            userFile = userLocFun(textObj.username, serverFile)
            if Paths.isfile(userFile):
                out = loadJsonFile(userFile, textObj)
                return out
    globalFile = globalLocFun(serverFile)
    if Paths.isfile(globalFile):
        out = loadJsonFile(globalFile, textObj)
        return out
    else:
        if textObj is not None:
            textObj.getError(err, globalFile)
        return None


def loadUserParFunFile(functionFile, GUIobj=None):
    return loadServerFile(functionFile, Paths.getUserParFunFile, Paths.getGlobalParFunFile,
                          'parFileNotExists', GUIobj)


def loadUserHdrFile(headerFile, GUIobj=None):
    return loadServerFile(headerFile, Paths.getUserHdrFile, Paths.getGlobalHdrFile,
                          'hdrFileNotExists', GUIobj)

def loadUserGraphFile(graphFile, GUIobj=None):
    return loadServerFile(graphFile, Paths.getUserGraphFile, Paths.getGlobalGraphFile,
                          'grfFileNotExists', GUIobj)

def loadUserSerFunFile(functionFile, GUIobj=None):
    return loadServerFile(functionFile, Paths.getUserSerFunFile, Paths.getGlobalSerFunFile,
                          'serFileNotExists', GUIobj)

def getServerFiles(pathArray, ext):
    serverFiles = []
    for path in pathArray:
        print(path, Paths.isdir(path))
        if Paths.isdir(path):
            print('a')
            for file in Paths.listdir(path, ext):
                fileWOExt = file.split('.', 1)[0]
                if fileWOExt not in serverFiles:
                    serverFiles.append(fileWOExt)
    return serverFiles



def getUserParFunFiles(textObj=None):
    paths = [Paths.globalParFun]
    if textObj is not None:
        if textObj.username is not None:
            paths.append(Paths.getUserParFunFold(textObj.username))
    return getServerFiles(paths, Paths.pfunExt)

def getUserHdrFiles(textObj=None):
    paths = [Paths.globalHeaders]
    if textObj is not None:
        if textObj.username is not None:
            paths.append(Paths.getUserHdrFold(textObj.username))
    return getServerFiles(paths, Paths.hdrExt)

def getUserSerFunFiles(textObj=None):
    paths = [Paths.globalSerFun]
    if textObj is not None:
        if textObj.username is not None:
            paths.append(Paths.getUserSerFunFold(textObj.username))
    return [""] + getServerFiles(paths, Paths.sfunExt)

def getUserGrfFiles(textObj=None):
    paths = [Paths.globalGraphs]
    if textObj is not None:
        if textObj.username is not None:
            paths.append(Paths.getUserGraphFold(textObj.username))
    return getServerFiles(paths, Paths.grfExt)

def getUserGUIFiles(textObj=None):
    if textObj is None:
        return {"settings": Paths.globalGUISettFile,
                "paths": Paths.globalGUIPathsFile}
    else:
        settFile, pathFile = checkUserGUIFiles(textObj)
        return {"settings": settFile,
                "paths": pathFile}

def checkUserGUIFiles(textObj=None):
    if textObj is not None:
        userFolder = Paths.getUserGUIFold(textObj.username)
        if not Paths.isdir(userFolder):
            os.mkdir(userFolder)
        userPathFile = Paths.getUserGUIPathFile(textObj.username)
        userSettFile = Paths.getUserGUISettFile(textObj.username)
        if not Paths.checkUserGUIFiles(textObj.username):
            shutil.copy(Paths.globalGUIPathsFile, userPathFile)
            shutil.copy(Paths.globalGUISettFile, userSettFile)
        return userSettFile, userPathFile
    return Paths.globalGUISettFile, Paths.globalGUIPathsFile

def loadUserGUIPreset(textObj=None):
    files = getUserGUIFiles(textObj)
    settings = loadJsonFile(files["settings"])
    paths = loadJsonFile(files["paths"])
    return settings, paths

def saveUserGUIPresets(settings, paths, textObj=None):
    if textObj is not None:
        saveJsonFile(Paths.getUserGUISettFile(textObj.username), settings)
        saveJsonFile(Paths.getUserGUIPathFile(textObj.username), paths)

def getGUIMeasPresets(textObj=None):
    settings, paths = loadUserGUIPreset(textObj)
    defSettings, defPaths = loadUserGUIPreset()
    guiPreset = {'currViewIdx': 0}
    for pathName in defPaths:
        if pathName in paths:
            guiPreset[pathName] = paths[pathName]
        else:
            guiPreset[pathName] = defPaths[pathName]
    for settName in defSettings:
        if settName in settings:
            guiPreset[settName] = settings[settName]
        else:
            guiPreset[settName] = defSettings[settName]
    return guiPreset  # {'folder': paths["dataFolder"],
    #         'currViewIdx': 0,
    #         'hdrFile': settings["headerFile"],
    #         'paramFile': settings["parameterFile"],
    #         'grfFile': settings["graphFile"],
    #         'sfunFile': settings["serFunFile"]
    #         }

def saveGUIMeasUserPreset(presets, textObj=None):
    if textObj is not None:
        settings, paths = loadUserGUIPreset(textObj)
        defSettings, defPaths = loadUserGUIPreset()
        for pathName in defPaths:
            paths[pathName] = presets[pathName]
        for settName in defSettings:
            settings[settName] = presets[settName]
        # settings["headerFile"] = presets['hdrFile']
        # settings["parameterFile"] = presets['paramFile']
        # settings["graphFile"] = presets['grfFile']
        # paths["dataFolder"] = presets['folder']
        # paths["serFunFile"] = presets['sfunFile']
        saveUserGUIPresets(settings, paths, textObj)

def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval

def naturalKeys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    float regex comes from https://stackoverflow.com/a/12643073/190597
    '''
    return [atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text)]

def naturalList(l):
    return [naturalKeys(k) for k in l]

def lessThan(value, compValue):
    value = value.replace(',', '.')
    compValue = compValue.replace(',', '.')
    l = [value, compValue]
    l.sort(key=naturalKeys)
    return value == l[0]

def sortIdx(seq):
    #http://stackoverflow.com/questions/3382352/equivalent-of-numpy-argsort-in-basic-python/3382369#3382369
    #by unutbu
    #print('a', seq.__getitem__)
    seq = naturalList(seq)
    return sorted(range(len(seq)), key=seq.__getitem__)

def rearrangeUp(lis):
    if lis is not None:
        temp = []
        for item in lis:
            temp.append(item.split('.', 1)[0].replace(',', '.'))
        #lis.sort(key=naturalKeys)
        a = sortIdx(temp)
        return array(lis)[a]
    else:
        return []

def isNumerical(var):
    return isinstance(var, numbers.Number)


if __name__ == "__main__":
    a = Paths.listdir("//10.110.8.81/AET-SI-TO-Izmenjava/Andrej_Mrak/__Nove_Meritve/968/968TTrekvalifikacija")
    rearrangeUp(a)
