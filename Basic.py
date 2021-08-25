# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 10:20:23 2021

@author: andmra2
"""
import json
import os
import re
from numpy import argsort, array

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

def getUserGrfFiles(textObj=None):
    paths = [Paths.globalGraphs]
    if textObj is not None:
        if textObj.username is not None:
            paths.append(Paths.getUserGraphFold(textObj.username))
    return getServerFiles(paths, Paths.grfExt)

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



if __name__ == "__main__":
    a = Paths.listdir("//10.110.8.81/AET-SI-TO-Izmenjava/Andrej_Mrak/__Nove_Meritve/968/968TTrekvalifikacija")
    rearrangeUp(a)
