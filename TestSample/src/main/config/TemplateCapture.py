'''
Copyright (c) 2021-2022 OVGU LIA
Author: Harish Kumar Pakala
This source code is licensed under the Apache License 2.0 (see LICENSE.txt).
This source code may use other Open Source software components (see LICENSE.txt).
'''

    
class TemplateCapture(object):
    
    def __init__(self,templateSubmodel,templateName,pyAAS):
        self.templateSubmodel = templateSubmodel
        self.templateName = templateName
        self.pyAAS = pyAAS
        self.templateInstance = {}
    
    def _retrieveRelevantSubmodelElem(self,elemCollection,elemName):
        for submodelElem in elemCollection["value"]: 
            if (submodelElem["modelType"]["name"] == "SubmodelElementCollection"):
                return self._retrieveRelevantSubmodelElem(submodelElem,elemName)
            if (elemName in submodelElem["idShort"]):
                return submodelElem
        return None
        
    def retrieveRelevantSubmodelElem(self,elemName):
        aasELem = "submodel"
        if (self.templateSubmodel["modelType"]["name"] == "SubmodelElementCollection"):
            aasELem = "value"
        for submodelElem in self.templateSubmodel[aasELem]:     
            if (submodelElem["modelType"]["name"] == "SubmodelElementCollection"):
                return self._retrieveRelevantSubmodelElem(submodelElem,elemName)
            if (elemName in submodelElem["idShort"]):
                return submodelElem
        return None
    
    def createCreatePropertyInformation(self,categoryTagInfo,categoryInstance):
        for templateElem in categoryTagInfo:
            sELem = self.retrieveRelevantSubmodelElem(templateElem)
            if (sELem is not None):
                categoryInstance[templateElem] = {"type" : "Property","value":sELem["value"]}
            else:
                categoryInstance[templateElem] = {"type" : "Property","value":"Test"} 
        return  categoryInstance
    
    def createMultiLanguagePropertyInformation(self,categoryTagInfo,categoryInstance):
        for templateElem in categoryTagInfo:
            sELem = self.retrieveRelevantSubmodelElem(templateElem)
            if (sELem is not None):
                langStrings = {}
                for langStrin in sELem["value"]["langString"]:
                    langStrings[langStrin["language"]] = langStrin["text"]
                categoryInstance[templateElem] = {"type" : "MLP","value":langStrings}
            else:
                categoryInstance[templateElem] = {"type" : "MLP","value":"Test"}            
        return  categoryInstance
    
    def createFileElementInformation(self,categoryTagInfo,categoryInstance):
        for templateElem in categoryTagInfo:
            sELem = self.retrieveRelevantSubmodelElem(templateElem)
            if (sELem is not None):
                categoryInstance[templateElem] = {"type" : "File","value":sELem["value"]}
            else:
                categoryInstance[templateElem] = {"type" : "File","value":"Test"} 
        return  categoryInstance
    
    def captureCategoryELements(self,categoryTagInfo):
        categoryInstance = {}
        if "Property" in  categoryTagInfo:
            categoryInstance = self.createCreatePropertyInformation(categoryTagInfo["Property"],categoryInstance)
        if "MLP" in categoryTagInfo:
            categoryInstance = self.createCreatePropertyInformation(categoryTagInfo["MLP"],categoryInstance)
        if "File" in categoryTagInfo:
            categoryInstance = self.createCreatePropertyInformation(categoryTagInfo["File"],categoryInstance)
        return categoryInstance
          
    def getTemplateInformation(self):
        self.templateInfo = self.pyAAS.aasConfigurer.templateData[self.templateName]
        for category in self.templateInfo:
            self.templateInstance[category] = self.captureCategoryELements(self.templateInfo[category])
        return self.templateInstance      