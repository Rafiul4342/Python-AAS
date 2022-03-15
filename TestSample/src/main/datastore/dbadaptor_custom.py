'''
Copyright (c) 2021-2022 Otto-von-Guericke-Universitat Magdeburg, Lehrstuhl Integrierte Automation
Author: Harish Kumar Pakala
This source code is licensed under the Apache License 2.0 (see LICENSE.txt).
This source code may use other Open Source software components (see LICENSE.txt).
'''
try:
    from datastore.aas_database_server import AAS_Database_Server
except ImportError:
    from main.datastore.aas_database_server import AAS_Database_Server

class DB_ADAPTOR(object):
    '''
    classdocs
    '''

    def __init__(self,pyAAS):
        '''
        Constructor
        '''
        self.pyAAS = pyAAS
        self.AAS_Database_Server = AAS_Database_Server(self.pyAAS)   

        self.col_AASX = self.AAS_Database_Server.createNewDataBaseColumn("AASX")
        self.col_Messages = self.AAS_Database_Server.createNewDataBaseColumn("messages")
        
        
## AAS related Entries
    def deleteAASDataColumn(self):
        try:
            insertResult = self.AAS_Database_Server.delete_one("AASX")
            if (insertResult["message"] == "failure"):
                returnMessageDict = {"message" : ["The AASX Column deletion is not executed properly."], "status": 201}
            elif (insertResult["message"] == "success"):
                returnMessageDict = {"message" : ["The Asset Administration Shell Column was deleted successfully"], "status": 200}
            else:
                returnMessageDict = {"message": ["Unexpected Internal Server Error"],"status":500}            
        except Exception as E:
            returnMessageDict = {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}
        return returnMessageDict
  
    def updateAASDataList(self):
        aasData = self.pyAAS.aasConfigurer.jsonData
        aasContentData = {}
        i = 0
        for aasEntry in aasData["assetAdministrationShells"]:
            aasEData = {}
            submodels = []
            aasEData["idShort"] = aasEntry["idShort"]
            try: aasEData["description"]  = aasEntry["description"] 
            except Exception as E: pass
            try: aasEData["identification"]  = aasEntry["identification"]
            except Exception as E: pass
            for submodelRef in aasEntry["submodels"]:
                for aasSubmodel in aasData["submodels"]:
                    if submodelRef["keys"][0]["value"] == aasSubmodel["identification"]["id"]:
                        submodels.append(aasSubmodel)
                aasEData["submodels"] = submodels
            assets = []
            for assetRef in aasEntry["asset"]:
                for aasAsset in aasData["assets"]:
                    try:
                        if assetRef["keys"][0]["value"] == aasAsset["identification"]["id"]:
                            assets.append(aasAsset)
                    except Exception as E: pass
                                              
                aasEData["assets"] = assets
            aasContentData[i] = aasEData
            i = i + 1
        self.pyAAS.aasContentData = aasContentData
        
    def updateAASDataColumn(self,aasData):
        try:
            insertResult = self.AAS_Database_Server.insert_one(self.col_AASX,aasData)
            if (insertResult["message"] == "failure"):
                returnMessageDict = {"message" : ["The AASX is not updated."], "status": 201}
            elif (insertResult["message"] == "success"):
                self.pyAAS.aasConfigurer.jsonData = aasData
                self.updateAASDataList()
                self.pyAAS.aasConfigurer.getNamePlateData()
                self.pyAAS.aasConfigurer.getDcumentationData()
                self.pyAAS.aasConfigurer.getAASList()                
                returnMessageDict = {"message" : ["The AASX is updated successfully"], "status": 200}
            else:
                returnMessageDict = {"message": ["Unexpected Internal Server Error"],"status":500}
        except Exception as E:
            returnMessageDict = {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}
        return returnMessageDict
        
    def deleteUpdateAASXColumn(self,aasData):
        deleteResponse = self.deleteAASDataColumn()
        if (deleteResponse["status"] == 200):
            updateResponse = self.updateAASDataColumn(aasData)
            if (updateResponse["status"] == 200):
                returnMessageDict = {"message" : ["The AASX updated successfully"], "status": 200}
            elif (updateResponse["status"] == 201):
                returnMessageDict = {"message" : ["The AASX is not updated"], "status": 201}
            else:
                returnMessageDict = {"message": ["Unexpected Internal Server Error"],"status":500}    
        else:
            returnMessageDict = {"message": ["Unexpected Internal Server Error"],"status":500}
        return returnMessageDict  
  
    def getAASXEntityById(self,entity,entityId,note):
        returnMessageDict = {}
        try:
            aasData = self.pyAAS.aasConfigurer.jsonData
            for eIter in aasData[entity]:
                if  entityId == eIter["identification"]["id"]:
                    return {"message" : [eIter], "status" : 200}
            returnMessageDict = {"message":[note + "with the passed Id not found"],"status":201}
        except Exception as E:
            returnMessageDict = {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}
        return returnMessageDict
   
    def getAASShellById(self,data):
        aasId = data["aasId"]
        try:
            return self.getAASXEntityById("assetAdministrationShells",aasId, "Asset Administration SHell")  
        except Exception as E:
            return {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}

    def getSubmodelById(self,data):
        submodelId = data["submodelId"]
        try:
            return self.getAASXEntityById("submodels",submodelId, "Submodel ")  
        except Exception as E:
            return {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}

    def getAASaasetInformationById(self,data):
        assetId = data["assetId"]
        try:
            return self.getAASXEntityById("assets",assetId, "Asset ")  
        except Exception as E:
            return {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}

    def deleteAASXEntityByID(self,entity,entityId,note):
        try:
            aasData = self.pyAAS.aasConfigurer.jsonData
            i = 0
            for eIter in aasData[entity]:
                if entityId == eIter["identification"]["id"]:
                    del aasData[entity][i]
                    updateResponse = self.deleteUpdateAASXColumn(aasData)
                    if (updateResponse["status"] == 200):
                        return {"message":[note +" is deleted succesfully"],"status":200}
                    else:
                        return updateResponse
                i = i + 1
            returnMessageDict = {"message":[note +"with passed id found"],"status":201}
        except Exception as E:
            returnMessageDict = {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}
        return returnMessageDict

    def deleteAASShellById(self,data):
        aasId = data["aasId"]
        try:
            return self.deleteAASXEntityByID("assetAdministrationShells",aasId, "Asset Administration SHell")  
        except Exception as E:
            return {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}

    def deleteSubmodelById(self,data):
        submodelId = data["submodelId"]
        try:
            return self.deleteAASXEntityByID("submodel",submodelId, "Submodel ")  
        except Exception as E:
            return {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}

    def deleteAASaasetInformationById(self,data):
        assetId = data["assetId"]
        try:
            return self.deleteAASXEntityByID("assets",assetId, "Asset ")  
        except Exception as E:
            return {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}

    def putAASXEntityByID(self,entity,entityId,entityData,note):
        try:
            deleteResponse = self.deleteAASXEntityByID(entity,entityId,note)
            if (deleteResponse["status"] == 500):
                return deleteResponse
            else:
                aasData = self.pyAAS.aasConfigurer.jsonData
                aasData[entity].append(entityData)
                updateResponse = self.deleteUpdateAASXColumn(aasData)
                return updateResponse
        except Exception as E:
            return {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}
 
    def putAASShellById(self,data):
        aasId = data["aasId"]
        updateData = data["updateData"]
        try:
            return self.putAASXEntityByID("assetAdministrationShells",aasId,updateData, "Asset Administration SHell")  
        except Exception as E:
            return {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}

    def putSubmodelById(self,data):
        submodelId = data["submodelId"]
        updateData = data["updateData"]
        try:
            return self.putAASXEntityByID("submodel",submodelId, updateData,"Submodel ")  
        except Exception as E:
            return {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}

    def putAASaasetInformationById(self,data):
        assetId = data["assetId"]
        updateData = data["updateData"]
        try:
            return self.putAASXEntityByID("assets",assetId,updateData, "Asset ")  
        except Exception as E:
            return {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}

    def getEntityList(self,entity,note):
        try:
            aasData = self.pyAAS.aasConfigurer.jsonData
            if (len(aasData[entity]) != 0):
                return {"message" : aasData[entity], "status" : 200}
            else:
                return {"message" : [note + "are registered"], "status" : 200}
        except Exception as E:
            returnMessageDict = {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}
        return returnMessageDict        

    def getSubmodels(self,data):
        return self.getEntityList("submodels", "No Submodels")
        
    def getAssetInformation(self,data):
        return self.getEntityList("assets", "No Assets")
    
    def getAllAASShell(self,data):
        return self.getEntityList("assetAdministrationShells" ,"No Asset Administration shells")
    
    def getSubmodelRefsByAASId(self,data):
        aasId = data["aasId"]
        try:
            returnRespone = self.getAASXEntityById("assetAdministrationShells",aasId, "Asset Administration SHell")
            if (returnRespone["status"] == 200):
                return {"message" : returnRespone["message"]["submodels"],"status":200}
            else:
                return returnRespone
        except Exception as E:
            return {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}        

    def getSubmodelRefsByIDByAASId(self,data):
        aasId = data["aasId"]
        submodelRefId = data["submodelRefId"]
        try:
            returnRespone = self.getAASXEntityById("assetAdministrationShells",aasId, "Asset Administration SHell")
            if (returnRespone["status"] == 200):
                for submodelRef in returnRespone["message"]["submodels"]:
                    if (submodelRefId == submodelRef["keys"][0]["value"]):
                        return {"message" : [submodelRef],"status":200}
                return {"message":"The Submodel Reference is not found", "status":201}
            else:
                return returnRespone
        except Exception as E:
            return {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}        
   
    def deleteSubmodelRefbyIdByAASId(self,data):
        aasId = data["aasId"]
        submodelRefId = data["submodelRefId"]
        try:
            returnRespone = self.getAASXEntityById("assetAdministrationShells",aasId, "Asset Administration SHell")
            if (returnRespone["status"] == 200):
                aasData = returnRespone["message"]
                i = 0
                for submodelRef in aasData["submodels"]:
                    if (submodelRefId == submodelRef["keys"][0]["value"]):
                        del aasData["submodels"][i]
                        putResponse = self.putAASShellById({"aasId":aasId,"updateData":aasData})
                        if (putResponse ["status"] == 200):
                            return {"message":"The Submodel Reference is delete", "status":200}
                        else:
                            return putResponse
                    i = i + 1
                return {"message":"The Submodel Reference is not found", "status":201}
            else:
                return returnRespone
        except Exception as E:
            return {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}            

    def putSubmodelRefbyIdByAASId(self,data):
        aasId = data["aasId"]
        submodelRefId = data["submodelRefId"]
        submodelRefData = data["updateData"]
        try:
            returnRespone = self.getAASXEntityById("assetAdministrationShells",aasId, "Asset Administration SHell")
            if (returnRespone["status"] == 200):
                aasData = returnRespone["message"]
                i = 0
                for submodelRef in aasData["submodels"]:
                    if (submodelRefId == submodelRef["keys"][0]["value"]):
                        del aasData["submodels"][i]
                    i = i + 1
                    aasData["submodels"].append(submodelRefData)
                putResponse = self.putAASShellById({"aasId":aasId,"updateData":aasData})
                if (putResponse ["status"] == 200):
                    return {"message":"The Submodel Reference is updated succesfully", "status":200}
                else:
                    return putResponse                
            else:
                return returnRespone
        except Exception as E:
            return {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}  

    
    def getSubmodeByIdlElements(self,data):
        try:    
            returnResponse = self.getSubmodelById(data)
            if (returnResponse["status"] == 200):
                submodelElements =  {}
                i = 0
                for submodelELem in returnResponse["message"][0]["submodelElements"]:
                    submodelElements[i] = submodelELem
                    i = i + 1
                return {"message" : [submodelElements], "status":200}
            else:
                return returnResponse
        except Exception as E:   
            return {"message": ["Unexpected Internal Error"+str(E)],"status":500}  

    def _retrieveSubmodelElement(self,submodelElement,idShortPath):
        if (len(idShortPath) == 0):
            return {"message":[submodelElement],"status":200}
        else:
            if (submodelElement["modelType"]["name"] == "SubmodelElementCollection"):
                i = 0
                for elem in submodelElement["value"]:
                    if (elem["idShort"] == idShortPath[0]):
                        return {"message":self._retrieveSubmodelElement(elem,idShortPath[1:]), "status" : 200}
                    i = i + 1
                return {"message":["The submodel element is not found"], "status" : 201} 
    
    def getSubmodelByIdElementByIdShortPath(self,data):
        idShortPath = data["idShortPath"].split(".")
        try:    
            returnResponse = self.getSubmodelById(data)
            if (returnResponse["status"] == 200):
                subElemResponse = {}
                submodel =  returnResponse["message"][0]
                for submodelElem in submodel["submodelElements"]:
                    for _idShortPath in idShortPath:
                        if (submodelElem["idShort"] == idShortPath[0]):
                            subElemResponse = self._retrieveSubmodelElement(submodelElem,idShortPath[1:])
                if subElemResponse["status"] == 201:
                    return {"message":["The submodel element is not found"], "status" : 201} 
                else :
                    checkLoop = True
                    response = subElemResponse
                    while checkLoop:
                        if "message" in response:
                            response = response["message"]
                        else:
                            return {"message":response,"status":200}
            else:
                return returnResponse
        except Exception as E:   
            return {"message": ["Unexpected Internal Error"+str(E)],"status":500}  

    def _retrievenUpdateSubmodelElement(self,submodelElement,idShortPath,submodelElemNew):
        if (len(idShortPath) == 0):
            return submodelElement
        else:
            if (submodelElement["modelType"]["name"] == "SubmodelElementCollection"):
                i = 0
                for elem in submodelElement["value"]:
                    if (elem["idShort"] == idShortPath[0]):
                        submodelElement["value"][i] = self._retrievenUpdateSubmodelElement(elem,idShortPath[1:],submodelElemNew)
                    i = i + 1
                return  submodelElement

    def putSubmodelByIdElementByIdShortPath(self,data):
        idShortPath = data["idShortPath"]
        if ("." in idShortPath):
            idShortPath = data["idShortPath"].split(".")
        else:
            idShortPath = [idShortPath]
        submodelElemNew = data["updateData"]
        try:    
            returnResponse = self.getSubmodelById(data)
            if (returnResponse["status"] == 200):
                submodel =  returnResponse["message"][0]
                i = 0
                for submodelElem in submodel["submodelElements"]:
                    for _idShortPath in idShortPath:
                        if (submodelElem["idShort"] == idShortPath[0]):
                            submodel["submodelElements"][i] = self._retrievenUpdateSubmodelElement(submodelElem,idShortPath[1:],submodelElemNew)
                    i = i + 1        
                return self.putSubmodelById({"updateData" :submodel,"submodelId":data["submodelId"]})
            else:
                return returnResponse
        except Exception as E:   
            return {"message": ["Unexpected Internal Error"+str(E)],"status":500}  

    def getSubmodelByIdElementByIdShortPathValue(self,data):
        idShortPath = data["idShortPath"]
        if ("." in idShortPath):
            idShortPath = data["idShortPath"].split(".")
        else:
            idShortPath = [idShortPath]
        try:    
            returnResponse = self.getSubmodelById(data)
            if (returnResponse["status"] == 200):
                subElemResponse = {}
                submodel =  returnResponse["message"][0]
                for submodelElem in submodel["submodelElements"]:
                    for _idShortPath in idShortPath:
                        if (submodelElem["idShort"] == idShortPath[0]):
                            subElemResponse = self._retrieveSubmodelElement(submodelElem,idShortPath[1:])
                if subElemResponse["status"] == 201:
                    return {"message":["The submodel element is not found"], "status" : 201} 
                else :
                    checkLoop = True
                    response = subElemResponse
                    while checkLoop:
                        if "message" in response:
                            response = response["message"]
                        else:
                            return {"message":[{"value":response[0]["value"]}],"status":200}
            else:
                return returnResponse
        except Exception as E:   
            return {"message": ["Unexpected Internal Error"+str(E)],"status":500}  

    def _retrievenUpdateSubmodelElementValue(self,submodelElement,idShortPath,submodelValue):
        if (len(idShortPath) == 0):
            submodelElement["value"] = submodelValue["value"]
            return submodelElement
        else:
            if (submodelElement["modelType"]["name"] == "SubmodelElementCollection"):
                i = 0
                for elem in submodelElement["value"]:
                    if (elem["idShort"] == idShortPath[0]):
                        submodelElement["value"][i] = self._retrievenUpdateSubmodelElementValue(elem,idShortPath[1:],submodelValue)
                    i = i + 1
                return  submodelElement
    
    def putSubmodelByIdElementByIdShortPathValue(self,data):
        idShortPath = data["idShortPath"]
        if ("." in idShortPath):
            idShortPath = data["idShortPath"].split(".")
        else:
            idShortPath = [idShortPath]
        submodelValue = data["updateData"]
        try:    
            returnResponse = self.getSubmodelById(data)
            if (returnResponse["status"] == 200):
                subElemResponse = {}
                submodel =  returnResponse["message"][0]
                i = 0
                for submodelElem in submodel["submodelElements"]:
                    for _idShortPath in idShortPath:
                        if (submodelElem["idShort"] == idShortPath[0]):
                            submodel["submodelElements"][i] = self._retrievenUpdateSubmodelElementValue(submodelElem,idShortPath[1:],submodelValue)
                    i = i + 1        
                return self.putSubmodelById({"updateData" :submodel,"submodelId":data["submodelId"]})
            else:
                return returnResponse
        except Exception as E:   
            return {"message": ["Unexpected Internal Error"+str(E)],"status":500}  
        

                      
    def saveNewConversationMessage(self,coversationId,messageType,messageId,message):
        message = {
                    "messageType" : messageType,
                    "message_Id" : messageId,
                    "message" : message,
                    "coversationId" : coversationId
                }
        returnMessageDict = {}
        try:
            response = self.AAS_Database_Server.insert_one(self.mongocol_Messages, message)
            returnMessageDict = {"message": ["The details are successfully recorded"],"status":200}            
        except Exception as E:
            returnMessageDict = {"message": ["Unexpected Internal Error"],"status":500}
        return returnMessageDict    
    
    def getMessageCount(self):
        try:
            messages = self.AAS_Database_Server.find(self.mongocol_Messages,{})
            if (messages["message"] == "success"):
                returnMessageDict = {"message": [len(messages["data"])],"status":200}
            else:
                returnMessageDict = {"message": [0],"status":200}
        except:
            returnMessageDict = {"message": [0],"status":500}
        return returnMessageDict   



## Message Level Entries


#### AASDescritpors Registry Start ######################

 
######### Submodel Registry API Services End ###############################


#AASsubmodel,AASsubmodelSubmodelElements,AASsubmodelSubmodelElementsValue,AASsubmodelSubmodelElementsByPath,AASsubmodelSubmodelElementsByPathValue
        
    def getAAsSubmodelbyIdSubmodelElem(self,data):
        submodelId = data["submodelId"]
        returnMessageDict = {}
        resultList = []
        resultListTemp = []
        try:
            aasSubmodels = self.getAAS(data)            
            for aas in aasSubmodels["message"]:
                for submodel in aas["submodels"]:
                    resultListTemp.append(submodel)

            if len(resultListTemp) == 0:
                returnMessageDict = {"message": ["No submodels are yet registered"],"status":500}
                
            else :
                for submodel in resultListTemp:
                    if submodel["idShort"] == submodelId or submodel["identification"]["id"] == submodelId :
                        for submodelElem in submodel["submodelElements"]:
                            resultListTemp.append(submodelElem)
                if len(resultList) == 0:
                    returnMessageDict = {"message": ["The AAS does not contain the specified submodel"],"status":500}
                else:
                    returnMessageDict = {"message": resultList,"status":200}
                
        except Exception as E:
            returnMessageDict = {"message": ["Unexpected Internal Server Error"+str(E)],"status":500}
        return returnMessageDict 

    def modifyRaddQual(self,submodelElement,qualifier):
        if "constraints" in list(submodelElement.keys()):
            i = 0
            qualpresent = False
            for qual in submodelElement["submodelElement"]["constraints"]:
                if (qual["type"] == qualifier["type"]):
                    submodelElement["constraints"][i]["value"] = qualifier["value"]
                    qualpresent = True
            if (not qualpresent):
                submodelElement["submodelElement"]["constraints"].append(qualifier)        
        return submodelElement

    def _retrievenUpdateSubmodelElementQual(self,submodelElement,idShortPath,qualifier):
        if (len(idShortPath) == 0):
            return self.modifyRaddQual(submodelElement,qualifier)
        else:
            if (submodelElement["modelType"]["name"] == "SubmodelElementCollection"):
                i = 0
                for elem in submodelElement["value"]:
                    if (elem["idShort"] == idShortPath[0]):
                        submodelElement["value"][i] = self._retrievenUpdateSubmodelElementQual(elem,idShortPath[1:],qualifier)
                    i = i + 1
                return  submodelElement
            else:
                return self.modifyRaddQual(submodelElement,qualifier)
        
    def putSubmodelElementQualbyId(self,data):
        idShortPath = data["idShortPath"]
        if ("." in idShortPath):
            idShortPath = data["idShortPath"].split(".")
        else:
            idShortPath = [idShortPath]
        qualifier = data["updateData"]
        try:    
            returnResponse = self.getSubmodelById(data)
            if (returnResponse["status"] == 200):
                submodel =  returnResponse["message"][0]
                i = 0
                for submodelElem in submodel["submodelElements"]:
                    for _idShortPath in idShortPath:
                        if (submodelElem["idShort"] == idShortPath[0]):
                            submodel["submodelElements"][i] = self._retrievenUpdateSubmodelElementQual(submodelElem,idShortPath[1:],qualifier)
                    i = i + 1        
                return self.putSubmodelById({"updateData" :submodel,"submodelId":data["submodelId"]})
            else:
                return returnResponse
        except Exception as E:   
            return {"message": ["Unexpected Internal Error"+str(E)],"status":500}  

    
    def getSubmodePropertyDict(self,submodel):
        submodelProperetyDict = {}
        for eachProperty in submodel["submodelElements"]:
            submodelProperetyDict[eachProperty["idShort"]] = self.processEachSubmodelElement(eachProperty)
        return submodelProperetyDict

   
if __name__ == "__main__":
    dba = DB_ADAPTOR()
    dba.getAAS()
    