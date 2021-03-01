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




# loads application settings file
with open(configFilePath) as json_file:
    settings = json.load(json_file)

# Folders
server = settings['paths']['server']
text = os.path.join(scriptDir, 'Text/')
dataProcessorDir = server + 'DataProcessor/'

globalDir = 'global/'

parameterFunctions = dataProcessorDir + 'ParameterFunctions/'
globalParFun = parameterFunctions + globalDir

headers = dataProcessorDir + 'Headers/'
globalHeaders = headers + globalDir

graphs = dataProcessorDir + 'Graphs/'
globalGraphs = graphs + globalDir

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
    return getUserParFunFold(username) + file + '.pfun'


# return parameter global function file
def getGlobalParFunFile(file):
    return globalParFun + file + '.pfun'


def getUserHdrFold(username):
    return headers + username + '/'


def getUserHdrFile(username, file):
    return  getUserHdrFold(username) + file + '.hdr'


def getGlobalHdrFile(file):
    return globalHeaders + file + '.hdr'

def getUserGraphFold(username):
    return graphs + username + '/'

def getUserGraphFile(username, file):
    return getUserGraphFold(username) + file + '.grf'


def getGlobalGraphFile(file):
    return globalGraphs + file + '.grf'


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


def listdir(directory):
    return humanSort(os.listdir(directory))






