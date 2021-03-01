# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 13:31:51 2021

@author: andmra2
"""

if __name__ == "__main__":
    import Paths
    from Basic import loadJsonFile
else:
    from . import Paths
    from .Basic import loadJsonFile





#availableLan, baseErrors = checkLanguages()
#errorText = loadText('Errors', availableLan, baseErrors)
#warningText = loadText('Warnings', availableLan, baseErrors)


class TextType(object):
    
    def __init__(self, textObj, lan):
        self.lan = 'en'
        self.text = {}
        self.availableLan = textObj.availableLan
        self.baseErrors = textObj.baseErrors
        self.getBasicText()
        self.setLan(lan)
        
        
        
    def setLan(self, lan):
        if lan in self.availableLan:
            self.lan = lan
            

    def getText(self, textType, *args):
        if textType in self.text:
            if self.lan in self.text[textType]:
                return self.text[textType][self.lan].format(*args)
            else:
                return self.getText('lanNotExists', self.lan, textType)
        else:
            return self.getText('txtTypeNotExists', textType)
    
    def loadText(self, file):
        lanText = {}
        for lan in self.availableLan:
            lanFile = Paths.getLanFile(lan, file)
            if Paths.isfile(lanFile):
                lanText[lan] = loadJsonFile(lanFile)
            else:
                lanText[lan] = {}
        
        if 'en' in self.availableLan:
            for text in lanText['en']:
                self.text[text] = {}
                for lan in self.availableLan:
                    if lan in lanText:
                        if text in lanText[lan]:
                            self.text[text][lan] = lanText[lan][text]
            for text in self.baseErrors['en']:
                self.text[text] = {}
                for lan in self.availableLan:
                    self.text[text][lan] = self.baseErrors[lan][text]
        else:
            self.text['lanNotExists']['en'] = 'There is no language available.'
            
    def getBasicText(self):
        for lan in self.baseErrors:
            for error in self.baseErrors[lan]:
                if error in self.text:
                    self.text[error][lan] = self.baseErrors[lan][error]
                else:
                    self.text[error] = {lan: self.baseErrors[lan][error]}
        
    
        
        
class ErrorText(TextType):
    
    def __init__(self, textObj, lan='en'):
        TextType.__init__(self, textObj, lan)
        self.loadText('Errors')
        
        
class WarningText(TextType):
    
    def __init__(self, textObj, lan='en'):
        self.text = textObj.baseErrors
        TextType.__init__(self, textObj, lan)
        self.loadText('Warnings')
        
class Text(object):
    
    def __init__(self, lan='en'):
        self.lan = 'en'
        self.availableLan = {}
        self.baseErrors = {}
        self.errorText = None
        self.warningText = None
        self.checkLanguages()
        self.errorText = ErrorText(self)
        self.warningText = WarningText(self)
        self.setLan(lan)
        
    def setLan(self, lan):
        if lan in self.availableLan:
            self.lan = lan
        self.errorText.setLan(lan)
        self.warningText.setLan(lan)
            
    def getError(self, textType, *args):
        if self.errorText is None:
            if 'en' in self.baseErrors:
                return self.baseErrors['en'][textType]
            else:
                return 'File {0} cannot be read.'.format(*args)
        else:
            return self.errorText.getText(textType, *args)
    
    def getWarning(self, textType, *args):
        return self.warningText.getText(textType, *args)
    
    def checkLanguages(self):
        for lan in Paths.listdir(Paths.text):
            if Paths.isdir(Paths.text+lan):
                lanCfgFile = Paths.getLanCfgFile(lan)
                if Paths.isfile(lanCfgFile):
                    settings = loadJsonFile(lanCfgFile, self)
                    if 'errors' in settings and 'lan' in settings:
                        if ('lanNotExists' in settings['errors'] and 
                            'txtTypeNotExists' in settings['errors']):
                            self.availableLan[lan] = settings['lan']
                            self.baseErrors[lan] = {'lanNotExists': settings['errors']['lanNotExists'],
                                               'txtTypeNotExists': settings['errors']['txtTypeNotExists']}
                            
    
    
    

class DebugTextObj(object):
    
    def __init__(self, lan, username=None):
        self.text = Text(lan)
        self.username = None
    
    def getError(self, errType, *args):
        print('Error:', self.text.getError(errType, *args))
        
    def getWarning(self, warnType, *args):
        print('Warning:', self.text.getWarning(warnType, *args))
        
    def moveErrorsToWarnings(self):
        pass 
    
# if Text object is not given (user sets language) use english Text object       
def getTextObj(textObj):
    if textObj is None:  
        return DebugTextObj(lan='en')
    return textObj



            
            





        
        
  


        

        
        

    


        
    
if __name__ == "__main__":
    
    text = Text('si')
    print(text.getWarning('undfHdrPar', 'sdfsf', 'dff'))
        
    
        
        