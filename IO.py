# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 13:23:08 2021

@author: andmra2
"""

from pandas import read_csv, to_timedelta
import os

if os.path.dirname(__file__) == os.getcwd():
    import Basic
    import Paths
    import Texts
else:
    from . import Paths
    from . import Basic
    from . import Texts

#from time import time

def transformPDHeader(pdg, headerFile, textObj=None):
    header = Basic.loadUserHdrFile(headerFile, textObj)
    textObj = Texts.getTextObj(textObj)
    if header is not None:
        for parameter in header:
            if "headers" in header[parameter]:
                for file in pdg:
                    for item in pdg[file]:
                        #print(item.strip(), header[parameter]["headers"], item.strip() in header[parameter]["headers"])
                        if item.strip() in header[parameter]["headers"]:
                            pdg[file] = pdg[file].rename(columns={item: parameter})
            else:
                textObj.getWarning('undfHdrFeat', parameter, headerFile)

    return pdg



# reads directory that contains txt files with pyrometer measurements
def readPyroDir(dirPath, textObj=None):
    output = {}  # initialize output dictionary
    textObj = Texts.getTextObj(textObj)  # if Text object is not given (user sets language) use english Text object
    if Paths.isdir(dirPath):  # if directory exists 
        for file in Basic.rearrangeUp(Paths.listdir(dirPath)):  # iterate trough its content
            out = readPyroFile(dirPath, file, textObj)  # try to read every item in the directory
            if out is not None:  # if file as been read 
                fileName = Basic.removeExt(file)  # get file name without extension
                output[fileName] = out  # store file content in a output dictionary
        textObj.moveErrorsToWarnings()
        return output  # return output dictionary, warnings list and None error
    else:  # if directory does not exist raise 'dirNotExists' error
        textObj.getError('dirNotExists', dirPath)
        return None  # return None
    
def readPyroFile(dirPath, file, GUIobj=None):
    output = None  # initialize output dictionary
    textObj = Texts.getTextObj(GUIobj)  # if Text object is not given (user sets language) use english Text object
    if Paths.isdir(dirPath):  # if directory exists
        if Basic.isTxt(file):  # if file is a txt file
            filePath = Basic.joinFilePath(dirPath, file)  # join directory path with file name
            if Paths.isfile(filePath):  # if file exists
                # TODO check if this could be replaced with some poandas built-in method: ',' in 'Čas' colum is the main problem
                with open(filePath, 'r') as fileR:  # read all file's content
                    fileContent = fileR.read()
                with open(filePath, 'w') as fileW: # replace all ',' with '.'
                    fileW.write(fileContent.replace(',', '.'))
                # read the file with pandas
                output = read_csv(filePath,
                                  delimiter='\t',
                                  encoding='windows-1250',
                                  #decimal=','
                                  )
                # transform "Čas" column to timedelta
                if 'Čas' in output:
                    try:  # if transformation is succesful store it in column 't'
                        output['t'] = to_timedelta(output['Čas']).dt.total_seconds()#.astype('timedelta64[s]')
                    except:  # if transformation is not succesful store 'Čas' column in column 't' and raise warning
                        output['t'] = output['Čas']
                        textObj.getWarning('timeFrmWrong', filePath)
                    output = output.drop(columns=['Čas'])
                return output
            textObj.getError('fileNotExists', filePath)  # if file does not exist raise fileNotExists error
            return output#  return output=None
        return output # if file is not txt return output=None
    textObj.getErrorText('dirNotExists', dirPath)  # if file does not exist raise 'dirNotExists' error
    return output  #  return output=None 

    
if __name__=="__main__":
    out = readPyroDir(Paths.testDir)
    
    if out is not None:
        print(out['H10'])
