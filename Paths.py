# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 10:10:03 2021

@author: andmra2
"""
import json
import re
import os
from os.path import isdir, isfile

import os


scriptDir = os.path.dirname(__file__) #<-- absolute dir the script is in

# Special files
configFile = 'settings.cfg'
configFilePath = os.path.join(scriptDir, configFile)

#  extensions
pfunExt = '.pfun'
hdrExt = '.hdr'
grfExt = '.grf'
setExt = '.set'


# loads application settings file
with open(configFilePath) as json_file:
    settings = json.load(json_file)

# Folders
server = settings['paths']['server']
text = os.path.join(scriptDir, 'Text/')
dataProcessorDir = server + 'DataProcessor/'
downloadPath = server + "Andrej_Mrak/DataProcessor"
adminFolderPath = server + 'Andrej_Mrak/ProgramData/DataProcessor/'
permissionFolder = adminFolderPath + 'Permissions/'
encryptionFolder = adminFolderPath + 'Encryption/'
newUserRequestsFolder = adminFolderPath + 'UserRequests/'
usersDatabase = adminFolderPath + 'UsersDatabase/'

globalDir = 'global/'

parameterFunctions = dataProcessorDir + 'ParameterFunctions/'
globalParFun = parameterFunctions + globalDir

headers = dataProcessorDir + 'Headers/'
globalHeaders = headers + globalDir

graphs = dataProcessorDir + 'Graphs/'
globalGraphs = graphs + globalDir

GUIsett = dataProcessorDir + "GUI/"
globalGUISett = GUIsett + globalDir
globalGUIPathsFile = globalGUISett + "paths" + setExt
globalGUISettFile = globalGUISett + "settings" + setExt

testDir = dataProcessorDir + 'DPtest/'


# returns language configuration file path
def getLanCfgFile(lan):
    return text+lan+'/'+lan+'.cfg'

# returns language text file path
def getLanFile(lan, file):
    return text+lan+'/'+file+'.txt'

# returns folder where user specific parameter functions files are stored
def getUserParFunFold(username):
    return parameterFunctions + username + '/'


# return parameter function file of an user
def getUserParFunFile(username, file):
    return getUserParFunFold(username) + file + pfunExt


# return parameter global function file
def getGlobalParFunFile(file):
    return globalParFun + file + pfunExt


def getUserHdrFold(username):
    return headers + username + '/'


def getUserHdrFile(username, file):
    return getUserHdrFold(username) + file + hdrExt


def getGlobalHdrFile(file):
    return globalHeaders + file + hdrExt

def getUserGraphFold(username):
    return graphs + username + '/'

def getUserGraphFile(username, file):
    return getUserGraphFold(username) + file + grfExt


def getGlobalGraphFile(file):
    return globalGraphs + file + grfExt

def getUserGUIFold(username):
    return GUIsett + username +'/'

def getUserGUIPathFile(username):
    return getUserGUIFold(username) + "paths" + setExt

def getUserGUISettFile(username):
    return getUserGUIFold(username) + "settings" + setExt

def checkUserGUIFiles(username):
    return isfile(getUserGUIPathFile(username)) and isfile(getUserGUISettFile(username))


def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    float regex comes from https://stackoverflow.com/a/12643073/190597
    '''
    return [atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text)]


#rearange text list with "human" sorting (implementation:
def humanSort(lis):
    if lis is not None:
        lis.sort(key=natural_keys)
        return lis
    else:
        return []


def listdir(directory, ext=None):
    fileList = humanSort(os.listdir(directory))
    if ext is None:
        return fileList
    else:
        extLen = len(ext)
        fileListExt = []
        for file in fileList:
            if file[-extLen:] == ext:
                fileListExt.append(file)
        return fileListExt






