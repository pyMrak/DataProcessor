# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 09:08:34 2021

@author: andmra2
"""
from Texts import Text


class GUIfunObj(object):
    
    def __init__(self, username):
        self.username = username
        self.error = None
        self.warnings = []
        self.text = Text()
        
    def setLan(self, lan):
        self.text.setLan(lan)
        
    def checkError(self):
        out = self.error
        self.error = None
        return out
    
    def checkWarnings(self):
        if self.checkWarnings:
            out = self.warnings.copy()
            self.warnings = []
            return out
        
    def storeWarnings(self, warnings):
        self.warnings += warnings
        
    def storeWarning(self, warning):
        self.warnings.append(warning)
        
    def storeError(self, error):
        self.error = error
        
    def getWarning(self, warnType, *args):
        self.storeWarning(self.text.getWarning(warnType, *args))
        
    def getError(self, errType, *args):
        self.storeError(self.text.getError(errType, *args))
        
    def moveErrorToWarnings(self):
        error = self.checkErrors()
        if error is not None:
            self.storeWarning(error)

            