# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 10:20:23 2021

@author: andmra2
"""
import json
import Paths





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


def loadUserParFunFile(functionFile, textObj=None):
    return loadServerFile(functionFile, Paths.getUserParFunFile, Paths.getGlobalParFunFile,
                          'parFileNotExists', textObj)


def loadUserHdrFile(headerFile, textObj=None):
    return loadServerFile(headerFile, Paths.getUserHdrFile, Paths.getGlobalHdrFile,
                          'hdrFileNotExists', textObj)

def loadUserGraphFile(graphFile, GUIobj=None):
    return loadServerFile(graphFile, Paths.getUserGraphFile, Paths.getGlobalGraphFile,
                          'hdrFileNotExists', GUIobj)