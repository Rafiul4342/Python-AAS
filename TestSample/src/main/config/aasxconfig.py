'''
Copyright (c) 2021-2022 OVGU LIA
Author: Harish Kumar Pakala
This source code is licensed under the Apache License 2.0 (see LICENSE.txt).
This source code may use other Open Source software components (see LICENSE.txt).
'''
import json
import os.path

try:
    from utils.utils import AASDescriptor
except ImportError:
    from main.utils.aaslog import AASDescriptor

try:
    from config.TemplateCapture import TemplateCapture
except ImportError:
    from main.config.TemplateCapture import TemplateCapture

enabledState = {"Y":True, "N":False}

class ConfigParser(object):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
        self.jsonData = {}
        self.templateData = {}
        self.namePlateProperties = [
                                    'ManufacturerName','ManufacturerTypName',
                                    'TypClass','SerialNo','ChargeId','CountryOfOrigin',
                                    'YearOfConstruction','PhysicalAddress','Marking_CE',
                                    'Marking_CRUUS','Marking_RCM'
                                    ]
        self.namePlatePhysicalAddress = [ 
                                            'CountryCode','Street','PostalCode','City','StateCounty'
                                        ]        
        with open(os.path.join(self.pyAAS.repository, "TestSample.json")) as json_file:
            self.jsonData = json.load(json_file)
        with open(os.path.join(self.pyAAS.template_repository, "documentationInfo.json")) as json_file_document:
            self.templateData["Documentation"] = json.load(json_file_document)
        with open(os.path.join(self.pyAAS.template_repository, "namplateInfo.json")) as json_file_nameplate:
            self.templateData["Nameplate"] = json.load(json_file_nameplate)
        with open(os.path.join(self.pyAAS.repository,"ass_JsonSchema.json")) as json_file_aas:
            self.aasJsonSchema  = json.load(json_file_aas)
        with open(os.path.join(self.pyAAS.repository,"aasShell_JsonSchema.json")) as json_file_aasShell:
            self.aasShell_JsonSchema  = json.load(json_file_aasShell)
        with open(os.path.join(self.pyAAS.repository,"asset_JsonSchema.json")) as json_file_asset:
            self.assetJsonSchema  = json.load(json_file_asset)
        with open(os.path.join(self.pyAAS.repository,"submodel_JsonSchema.json")) as json_file_submodel:
            self.submodelJsonSchema  = json.load(json_file_submodel)
        with open(os.path.join(self.pyAAS.base_dir,"config/status.json")) as statusFile:
            self.submodel_statusResponse  = json.load(statusFile)
        with open(os.path.join(self.pyAAS.base_dir,"config/SrSp.json")) as SrSp_Path:
            self.SrSp  = json.load(SrSp_Path)    
            del self.SrSp["temp"]
        with open(os.path.join(self.pyAAS.dataRepository,"database.json")) as json_file_dataBase:
            self.dataBaseFile  = json.load(json_file_dataBase)
    
    def getStatusResponseSubmodel(self):
        return self.submodel_statusResponse
        
    def setExternalVariables(self,environ):
        for env_variable in environ.keys():
            try:
                if (env_variable.split("_")[0] == "LIA"):
                    self.pyAAS.lia_env_variable[env_variable] = os.environ[env_variable]
            except Exception as E:
                pass

    def configureAASJsonData(self):
        try:
            colCheck = self.pyAAS.dba.AAS_Database_Server.checkforExistenceofColumn("AASX")         
            if (colCheck == "empty column"):
                self.pyAAS.dba.updateAASDataColumn(self.jsonData)
            elif (colCheck == "data present"):
                self.pyAAS.dba.deleteAASDataColumn()
                self.pyAAS.dba.updateAASDataColumn(self.jsonData)
            elif (colCheck == "column not present"):
                self.pyAAS.dba.createNewDataBaseColumn("AASX")
                self.pyAAS.dba.updateAASDataColumn(self.jsonData)
            self.pyAAS.dba.updateAASDataList()
            self.getNamePlateData()
            self.getDcumentationData()
            self.getAASList()
            return True    
        except Exception as E:
            self.pyAAS.serviceLogger.info('Error configuring the database' + str(E))
            return False        
        
    def getAASEndPoints(self):
        aasEndpointsList = []
        moduleDict = {"MQTT":".mqtt_endpointhandler","RESTAPI":".restapi_endpointhandler"}
        for moduleName in moduleDict.keys():
            aasEndpointsList.append({"Name":moduleName,"Module":moduleDict[moduleName]})
        return aasEndpointsList

    def getAssetAccessEndPoints(self):
        return {"OPCUA":".io_opcua"}

    
    def getpropertyValue(self,submodelElement):
        check = True
        if (submodelElement["modelType"]["name"] == "MultiLanguageProperty"):
            for lang in submodelElement["value"]["langString"]: 
                if lang["language"] == "de":
                    return lang["text"]
            if (check):
                return submodelElement["langString"]["0"]["value"]
        else:
            return submodelElement["value"]

    
    def getDcumentationData(self):
        for aasIndex in self.pyAAS.aasContentData.keys():
            aasN = self.pyAAS.aasContentData[aasIndex]
            documentationList = []
            for submodel in aasN["submodels"]:
                if "Documentation" in submodel["idShort"]:
                    for eachDocument in submodel["submodelElements"]:
                        tc = TemplateCapture(eachDocument,"Documentation",self.pyAAS)
                        documentationList.append(tc.getTemplateInformation())
            numberofDocuments =len(documentationList)
            if numberofDocuments == 0:
                self.pyAAS.documentationData[aasIndex] = []
            elif numberofDocuments == 1:
                self.pyAAS.documentationData[aasIndex] = [documentationList[0]]
            else:
                documentDivisions = []
                if ((numberofDocuments % 2) == 0):
                    for i in range(1,int(numberofDocuments/2)+1):
                        tempList = []
                        tempList.append(documentationList[2*i-2])
                        tempList.append(documentationList[2*i-1])
                        documentDivisions.append(tempList)
                else: 
                    numberofRows = int( (numberofDocuments + 1)/ 2)
                    for i in range(1,numberofRows):
                        tempList = []
                        tempList.append(documentationList[2*i-2])
                        tempList.append(documentationList[2*i-1])
                        documentDivisions.append(tempList)
                    documentDivisions.append(documentationList[numberofDocuments-1])
                self.pyAAS.documentationData[aasIndex] =  documentDivisions
                  
    def getNamePlateData(self):
        for aasIndex in self.pyAAS.aasContentData.keys():
            aasN = self.pyAAS.aasContentData[aasIndex]
            namePlateData = {}
            for namePlateProperty in self.namePlateProperties:
                for submodel in aasN["submodels"]:
                    if submodel["idShort"] == "Nameplate":
                        for submodelElement in submodel["submodelElements"]:
                            if  submodelElement["idShort"] == "PhysicalAddress":
                                for pAElement in submodelElement["value"]:
                                    self.pyAAS.namePlateData[pAElement["idShort"]] = self.getpropertyValue(pAElement)
                                
                            elif submodelElement["idShort"] == "Marking_CE":
                                pass
                            elif submodelElement["idShort"] == "Marking_CRUUS":
                                pass
                            elif submodelElement["idShort"] == "Marking_RCM":
                                pass
                            elif submodelElement["idShort"] == namePlateProperty:
                                namePlateData[namePlateProperty] = self.getpropertyValue(submodelElement)
            self.pyAAS.namePlateData[aasIndex] = namePlateData
 
    
    def GetAAsxSkills(self):
        skillListAAS= {}
        for aasIndex in self.pyAAS.aasContentData.keys():
            skillsDict = {}
            aasN = self.pyAAS.aasContentData[aasIndex]
            namePlateData = {}
            for subnmodel in aasN["submodels"]:
                if subnmodel["idShort"] == "OperationalData":
                    for eachskill in subnmodel["submodelElements"]:
                        skillName = ""
                        skill = {}
                        for skillDetails in eachskill["value"]: 
                            if (skillDetails["idShort"] == "SkillName"):
                                skill[skillDetails["idShort"]] = skillDetails["value"]
                                skillName = skillDetails["value"]
                            if (skillDetails["idShort"] == "SkillService"):
                                skill[skillDetails["idShort"]] = skillDetails["value"]
                            if (skillDetails["idShort"] == "InitialState"):
                                skill[skillDetails["idShort"]] = skillDetails["value"]
                            if (skillDetails["idShort"] == "enabled"):
                                skill[skillDetails["idShort"]] = enabledState[skillDetails["value"]] 
                        skillsDict[skillName] = skill
                        if (self.checkForOrderExistence(skill)):
                            self.pyAAS.productionStepList.append(skillName)
            else:
                pass                   
            productionSkill = {
                                "SkillName":"ProductionManager",
                                "SkillService":"Production Management",
                                "InitialState": "WaitforNewOrder",
                                "enabled":"Y"
                              }
            registerSkill = {
                                "SkillName":"Register",
                                "SkillService":"Register with the Registry Server",
                                "InitialState": "WaitforNewOrder",
                                "enabled":"Y"
                              }
            
            for key in self.SrSp.keys():
                skillsDict[key] = self.SrSp[key]
                if (self.checkForOrderExistence(self.SrSp[key])):
                    self.pyAAS.productionStepList.append(key)
            
            skillsDict["ProductionManager"] = productionSkill
            skillsDict["Register"] = registerSkill
            self.pyAAS.productionStepList.append("Register")
            skillListAAS[aasIndex] = skillsDict
        return skillListAAS 
    
    def getAASList(self):
        aasList = []
        i = 0
        for aasId in self.pyAAS.aasContentData:
            aasList.append({"aasId":aasId,"idShort":self.pyAAS.aasContentData[aasId]["idShort"]}) 
        numberofAAS = len(aasList)
        if numberofAAS == 0:
            self.pyAAS.AASData.append([])
        elif numberofAAS == 1:
            self.pyAAS.AASData.append(aasList)
        else:
            aasDivisions = []
            if ((numberofAAS % 2) == 0):
                for i in range(1,int(numberofAAS/2)+1):
                    tempList = []
                    tempList.append(aasList[2*i-2])
                    tempList.append(aasList[2*i-1])
                self.pyAAS.AASData.append(tempList)
            else: 
                numberofRows = int( (numberofAAS + 1)/ 2)
                for i in range(1,numberofRows):
                    tempList = []
                    tempList.append(aasList[2*i-2])
                    tempList.append(aasList[2*i-1])
                    aasDivisions.append(tempList)
                self.pyAAS.AASData.append(aasList[numberofAAS-1])
                 
        return self.pyAAS.AASData
        
    def getRelevantSubModel(self,submodelId):
        checkVar = False
        for submodel in self.jsonData["submodels"]:         
            if (submodel["identification"]["id"] == submodelId):
                checkVar = True
                return {"data" : submodel, "check" : True}
        if(not checkVar):
            return {"check" : False}
        
    def GetAAS(self):
        return self.jsonData
       
    def getSubModelbyID(self,sbIdShort):
        checkVar = True
        for submodel in self.jsonData["submodels"]:         
            if (submodel["idShort"] == sbIdShort):
                checkVar = False
                return submodel
        if(checkVar):
            return {"message": "Submodel with the given IdShort is not part of this AAS","status": 400}
    
  
    def getQualifiersList(self,submodelElem):
        qualiferList = {}
        if "constraints" in list(submodelElem.keys()):
            for qualifier in submodelElem["constraints"]:
                qualiferList[qualifier["type"]] = qualifier["value"]
        return (qualiferList)
    
    def getSemanticIdList(self,submodelElem):
        semanticIdList = {}
        if "semanticId" in list(submodelElem.keys()):        
            for semId in submodelElem["semanticId"]["keys"]:
                semanticIdList[semId["type"]]  = semId["value"]
        return (semanticIdList)
    
    def processSubmodelELement(self,submodelElement,submodelProperetyDict):
            if submodelElement["modelType"]["name"] == "SubmodelElementCollection":
                collectionDict = {}
                for elem in submodelElement["value"]: 
                    collectionDict = self.processSubmodelELement(elem,collectionDict)
                submodelProperetyDict[submodelElement["idShort"]+"**"+"Coll"] =  { "data" :  collectionDict,"qualifierList":self.getQualifiersList(submodelElement),"semanticIdList":self.getSemanticIdList(submodelElement), "type" : "collection" }
            elif (submodelElement["modelType"]["name"] == "Property"):
                submodelProperetyDict[submodelElement["idShort"]+"**"+"Prop"] =  {"data" : submodelElement["value"],"qualifierList":self.getQualifiersList(submodelElement),"semanticIdList":self.getSemanticIdList(submodelElement),"type" :"elem"}
            elif (submodelElement["modelType"]["name"] == "Range"):
                submodelProperetyDict[submodelElement["idShort"]+"**"+"Range"] =  {"data" : "test","qualifierList":self.getQualifiersList(submodelElement),"semanticIdList":self.getSemanticIdList(submodelElement),"type" :"elem"}
            elif (submodelElement["modelType"]["name"] == "MultiLanguageProperty"):
                submodelProperetyDict[submodelElement["idShort"]+"**"+"MultiLanguageProperty"] =  {"data" : submodelElement["value"],"qualifierList":self.getQualifiersList(submodelElement),"semanticIdList":self.getSemanticIdList(submodelElement),"type" :"elem"}
            elif (submodelElement["modelType"]["name"] == "File"):
                submodelProperetyDict[submodelElement["idShort"]+"**"+"File"] =  {"data" : submodelElement["value"],"qualifierList":self.getQualifiersList(submodelElement),"semanticIdList":self.getSemanticIdList(submodelElement),"type" :"elem"}
            elif (submodelElement["modelType"]["name"] == "Blob"):
                submodelProperetyDict[submodelElement["idShort"]+"**"+"Blob"] =  {"data" : submodelElement["value"],"qualifierList":self.getQualifiersList(submodelElement),"semanticIdList":self.getSemanticIdList(submodelElement),"type" :"elem"}
            elif (submodelElement["modelType"]["name"] == "ReferenceElement"):
                submodelProperetyDict[submodelElement["idShort"]+"**"+"ReferenceElement"] =  {"data" : submodelElement["value"],"qualifierList":self.getQualifiersList(submodelElement),"semanticIdList":self.getSemanticIdList(submodelElement),"type" :"elem"}
            elif (submodelElement["modelType"]["name"] == "RelationshipElement"):
                submodelProperetyDict[submodelElement["idShort"]+"**"+"RelationshipElement"] =  {"data" : submodelElement["value"],"qualifierList":self.getQualifiersList(submodelElement),"semanticIdList":self.getSemanticIdList(submodelElement),"type" :"elem"}
            elif (submodelElement["modelType"]["name"] == "AnnotatedRelationshipElement"):
                submodelProperetyDict[submodelElement["idShort"]+"**"+"AnnotatedRelationshipElement"] =  {"data" : submodelElement["value"],"qualifierList":self.getQualifiersList(submodelElement),"semanticIdList":self.getSemanticIdList(submodelElement),"type" :"elem"}
            elif (submodelElement["modelType"]["name"] == "Capability"):
                submodelProperetyDict[submodelElement["idShort"]+"**"+"Capability"] =  {"data" : "Capability","qualifierList":self.getQualifiersList(submodelElement),"semanticIdList":self.getSemanticIdList(submodelElement),"type" :"elem"}
            elif (submodelElement["modelType"]["name"] == "Operation"):
                submodelProperetyDict[submodelElement["idShort"]+"**"+"Operation"] =  {"data" : submodelElement["value"],"qualifierList":self.getQualifiersList(submodelElement),"semanticIdList":self.getSemanticIdList(submodelElement),"type" :"elem"}
            elif (submodelElement["modelType"]["name"] == "BasicEvent"):
                submodelProperetyDict[submodelElement["idShort"]+"**"+"BasicEvent"] =  {"data" : submodelElement["value"],"qualifierList":self.getQualifiersList(submodelElement),"semanticIdList":self.getSemanticIdList(submodelElement),"type" :"elem"}
            elif (submodelElement["modelType"]["name"] == "Entity"):     
                submodelProperetyDict[submodelElement["idShort"]+"**"+"Entity"] =  {"data" : submodelElement["value"],"qualifierList":self.getQualifiersList(submodelElement),"semanticIdList":self.getSemanticIdList(submodelElement),"type" :"elem"}    
            return submodelProperetyDict
            
    def getSubmodePropertyDict(self,submodel):
        submodelProperetyDict = {}
        for eachSubmodelElem in submodel["submodelElements"]:
            self.processSubmodelELement(eachSubmodelElem,submodelProperetyDict)
        return submodelProperetyDict
    
    def getSubmodelPropertyList(self,aasIdentifier):
        submodelNameList = []
        for submodel in self.pyAAS.aasContentData[aasIdentifier]["submodels"]:
            submodelNameList.append(submodel)
        return submodelNameList
    
    def getSubmodelPropertyListDict(self,aasIdentifier):
        submodelPropertyListDict = {}
        i = 0
        submodelList = self.getSubmodelPropertyList(aasIdentifier)
        for submodel in submodelList:
            submodelName =  submodel["idShort"]
            if not (submodelName in ["Nameplate","TechnicalData","Documentation"]):
                submodelProperetyDict = self.getSubmodePropertyDict(submodel)    
                if (i == 0):
                    status = " fade show active"
                    i = 1        
                else:
                    status = " fade show"
                submodelPropertyListDict[submodelName] = {"status" : status,
                                                          "data" : submodelProperetyDict,
                                                          "type" : "collection"
                                                         }
        return submodelPropertyListDict
    
    def configureDescriptor(self):
        aasDesc = AASDescriptor(self.pyAAS)
        return aasDesc.createDescriptor()

    def checkForOrderExistence(self,skill):
        if (skill["InitialState"] == "WaitforNewOrder"):
            return True
        else :
            return False
    
    def checkSubmodelwithOnlyPropeties(self,submodelName):
        returnData = self.getRelevantSubModel(submodelName)
        try:
            if returnData["check"] :
                submodelData = returnData["data"]
                for submodelElement in submodelData["submodelElements"]:
                    if submodelElement["modelType"]["name"] == "Property":
                        pass
                    else:
                        return False
                return True
            else:
                return False
        except Exception as E:
            self.pyAAS.serviceLogger.info("Error "+ str(E))
            return False      
          
    def saveToDatabase(self,dataJ):
        try:
            with open(os.path.join(self.pyAAS.dataRepository,"database.json"), 'w', encoding='utf-8') as databaseFile:
                json.dump(dataJ, databaseFile, ensure_ascii=False, indent=4)
                return {"message":"success"}
        except Exception as E: 
            return {"message":"failure"}  