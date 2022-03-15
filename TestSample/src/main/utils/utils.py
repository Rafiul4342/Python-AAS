'''
Copyright (c) 2021-2022 OVGU LIA
Author: Harish Kumar Pakala
This source code is licensed under the Apache License 2.0 (see LICENSE.txt).
This source code may use other Open Source software components (see LICENSE.txt).
'''

from jsonschema import validate
import uuid

try:
    from utils.i40data import Generic
except ImportError:
    from main.utils.i40data import Generic

class ExecuteDBModifier(object):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
            
    def executeModifer(self,instanceData):
        self.instanceId = str(uuid.uuid1())
        self.pyAAS.dataManager.pushInboundMessage({"functionType":1,"instanceid":self.instanceId,
                                                            "data":instanceData["data"],
                                                            "method":instanceData["method"]})
        vePool = True
        while(vePool):
            if (len(self.pyAAS.dataManager.outBoundProcessingDict.keys())!= 0):
                if (self.pyAAS.dataManager.outBoundProcessingDict[self.instanceId] != ""):
                    modiferResponse = self.pyAAS.dataManager.outBoundProcessingDict[self.instanceId]
                    del self.pyAAS.dataManager.outBoundProcessingDict[self.instanceId]
                    vePool = False
        return modiferResponse

class ProductionStepOrder(object):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
        self.gen = Generic() 
        
    def createProductionStepOrder(self):
        conversationCount = self.pyAAS.dba.getConversationCount()["message"][0]
        conversationId = "ProductionOrder" +"_"+ str(int(conversationCount) + 1)  
        
        #creating new conversation in the database
        self.pyAAS.dba.createNewConversation(conversationId)
        #append the new conversation to the conversationId List
        self.pyAAS.conversationIdList.append(conversationId) 
        if (len(self.pyAAS.conversationIdList) > 5 ):
            del self.pyAAS.conversationIdList[0] # if length of conversation id list is greater than 0 delete an element  
                
        DataFrame =      {
                                "semanticProtocol": "update",
                                "type" : "ProductionOrder",
                                "messageId" : "ProductionOrder_"+str(self.pyAAS.dba.getMessageCount()["message"][0]+1),
                                "SenderAASID" : self.pyAAS.AASID,
                                "SenderRolename" : "ProductionManager",
                                "conversationId" : conversationId,
                                "replyBy" :  "Internal",
                                "replyTo" :"Internal",
                                "ReceiverAASID" :  self.pyAAS.AASID,
                                "ReceiverRolename" : "ProductionManager"
                            }
        
        frame = self.gen.createFrame(DataFrame)
        self.I40OutBoundMessage = {"frame": frame,"interactionElements":[]}            
        self.pyAAS.msgHandler.putIbMessage(self.I40OutBoundMessage)
        return conversationId

class SubmodelUpdate(object):
    
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
        
    def update(self,submodelData,submodelId):
        try:
            submodels = {"submodels":[submodelData]}
            edm = ExecuteDBModifier(self.pyAAS)
            dataBaseResponse = edm.executeModifer({"data":{"updateData":submodels,"aasId":self.pyAAS.AASID},"method":"putSubmodels"})         
            return dataBaseResponse
        except Exception as e:
            return {"message" : ["Error Updating the Details"], "status" : 500}
    
    def modify(self,submodelId,propertyName,newValue):
        submodelDataResponse = self.pyAAS.dba.getSubmodelsbyId({"submodelId":submodelId,"updateData":"emptyData","aasId":self.pyAAS.AASID})
        if (submodelDataResponse["status"] == 500):
            return submodelDataResponse
        else:
            submodelData = submodelDataResponse["message"][0]
            updateCheck = False
            i = 0
            for submodelElement in submodelData["submodelElements"]:
                if propertyName == submodelElement["idShort"]:
                    submodelData["submodelElements"][i]["value"] = newValue
                    updateCheck = True
                i = i + 1
            submodelData
            if (updateCheck):
                submodels = {"submodels":[submodelData]}
                edm = ExecuteDBModifier(self.pyAAS)
                dataBaseResponse = edm.executeModifer({"data":{"updateData":submodels,"aasId":self.pyAAS.AASID},"method":"putSubmodels"})         
                return dataBaseResponse
    
    def delete(self,propertyName,submodelId):
        submodelDataResponse = self.pyAAS.dba.getSubmodelsbyId({"submodelId":submodelId,"updateData":"emptyData","aasId":self.pyAAS.AASID})
        i = 0
        if (submodelDataResponse["status"] == 500):
            return submodelDataResponse
        else:
            submodelData = submodelDataResponse["message"][0]
            for submodelElement in submodelData["submodelElements"]:
                if propertyName == submodelElement["idShort"]:
                    del submodelData["submodelElements"][i]
                    i = i + 1
            submodels = {"submodels":[submodelData]}
            edm = ExecuteDBModifier(self.pyAAS)
            dataBaseResponse = edm.executeModifer({"data":{"updateData":submodels,"aasId":self.pyAAS.AASID},"method":"putSubmodels"})         
            return dataBaseResponse
    
class SubmodelElement(object):
    
    def __init__(self,IdShort,Value,SemanticId,pyAAS):
        self.IdShort = IdShort
        self.Value = Value
        self.SemanticId = SemanticId
        self.pyAAS = pyAAS
    
    def create(self):
        submodelElem =   {
                          "value": self.Value,
                          "semanticId": {
                            "keys": [
                              {
                                "type": "GlobalReference",
                                "local": False,
                                "value": self.SemanticId,
                                "index": 0,
                                "idType": "IRDI"
                              }
                            ],
                            "First": {
                              "type": "GlobalReference",
                              "local": False,
                              "value": self.SemanticId,
                              "index": 0,
                              "idType": "IRDI"
                            },
                            "Last": {
                              "type": "GlobalReference",
                              "local": False,
                              "value": self.SemanticId,
                              "index": 0,
                              "idType": "IRDI"
                            }
                          },
                          "idShort": self.IdShort,
                          "modelType": {
                            "name": "Property"
                          },
                          "valueType": {
                            "dataObjectType": {
                              "name": ""
                            }
                          },
                          "kind": "Instance"
                        }
        return submodelElem
    
    def addSubmodelElement(self,submodelElement,submodelId):
        try:
            submodelPropertyList = self.pyAAS.dba.getSubmodelsbyId({"submodelId":submodelId,"updateData":"emptyData","aasId":self.pyAAS.AASID})
            if (submodelPropertyList["status"] == 200):
                submodelProperty = submodelPropertyList["message"][0]
                submodelProperty["submodelElements"].append(submodelElement)
                return {"message" : submodelProperty, "status" : 200} 
            else:
                return {"message" : "error", "status" : 500}
        except Exception as E:
            print(str(E))    

class AASDescriptor(object):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def createAASDescriptorElement(self,desc,aasDescriptor,aasxData):
        try:
            aasDescriptor[desc] = aasxData[desc]
        except Exception as e:
            pass
        return aasDescriptor

    def createSubmodelDescriptorElement(self,desc,sumodelDescriptor,submodel):
        try:
            sumodelDescriptor[desc] = submodel[desc]
        except:
            pass
        return sumodelDescriptor
    
    def createDescriptor(self):
        aasDescriptorList = []
        for aasxIndex in  self.pyAAS.aasContentData:
            aasxData = self.pyAAS.aasContentData[aasxIndex]
            aasDescriptor = {}
            descList = ["idShort","identification","description"]
            for desc in descList:
                aasDescriptor = self.createAASDescriptorElement(desc,aasDescriptor,aasxData)
    
            ip = self.pyAAS.lia_env_variable["LIA_AAS_RESTAPI_HOST_EXTERN"]
            port = self.pyAAS.lia_env_variable["LIA_AAS_RESTAPI_PORT_EXTERN"]
            descString = "http://"+ip+":"+port+"/aas/"+self.pyAAS.AASID 
            
            endpointsList = []
            submodelDescList = []
            
            endpointsList.append({"address": descString,"type": "restapi"})
            if (self.pyAAS.lia_env_variable["LIA_PREFEREDI40ENDPOINT"] == "MQTT"):
                pass
            else:
                endpointsList.append({"address": "http://"+ip+":"+port+"/i40commu","type": "communication"})  
      
            aasDescriptor["endpoints"]  =  endpointsList
            
            for submodel in aasxData["submodels"]:
                sumodelDescriptor = {}
                for desc in descList:
                    sumodelDescriptor = self.createSubmodelDescriptorElement(desc, sumodelDescriptor, submodel)
                sumodelDescriptor = self.createSubmodelDescriptorElement("semanticId", sumodelDescriptor, submodel)
                submodeldescString = descString +"/submodels/"+sumodelDescriptor["idShort"]
                sumodelDescriptor["endpoints"]  = [{
                                            "address": submodeldescString,
                                            "type": "restapi"
                                          }] 
                submodelDescList.append(sumodelDescriptor)
            
            aasDescriptor["submodelDescriptors"] = submodelDescList
            aasDescriptor["assets"] = aasxData["assets"]
            aasDescriptorList.append(aasDescriptor)
        return aasDescriptor

class DescriptorValidator(object):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def valitdateAASDescriptor(self,aasDescData):
        try :
            aasDescSchema = self.pyAAS.aasConfigurer.aasDescSchema
            if(not validate(instance = aasDescData, schema= aasDescSchema)):
                return True
            else:
                return False
        except Exception as E:
            return False
    
    def valitdateSubmodelDescriptor(self,submodelDescData):
        try :
            submodelDescSchema = self.pyAAS.aasConfigurer.submodelDescSchema
            if(not validate(instance = submodelDescData, schema= submodelDescSchema)):
                return True
            else:
                return False
        except Exception as E:
            return False

class AASMetaModelValidator(object):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def validateAASShell(self,aasShellData):
        try :
            aasShell_JsonSchema = self.pyAAS.aasConfigurer.aasShell_JsonSchema
            if(not validate(instance = {"assetAdministrationShells":[aasShellData]}, schema= aasShell_JsonSchema)):
                return True
            else:
                return False
        except Exception as E:
            return False

    
    def valitdateAAS(self,aasData):
        try :
            aasJsonSchema = self.pyAAS.aasConfigurer.aasJsonSchema
            if(not validate(instance = aasData, schema= aasJsonSchema)):
                return True
            else:
                return False
        except Exception as E:
            return False
    
    def valitdateSubmodel(self,submodelData):
        try :
            submodelJsonSchema = self.pyAAS.aasConfigurer.submodelJsonSchema
            if(not validate(instance = {"submodels":[submodelData]}, schema= submodelJsonSchema)):
                return True
            else:
                return False
        except:
            return False

    def valitdateAsset(self,assetData):
        try :
            assetJsonSchema = self.pyAAS.aasConfigurer.assetJsonSchema
            if(not validate(instance = {"assets": assetData}, schema= assetJsonSchema)):
                return True
            else:
                return False
        except:
            return False       

class ExecuteDBRetriever(object):
    def __init__(self,pyAAS):
        self.instanceId = str(uuid.uuid1())
        self.pyAAS = pyAAS
            
    def execute(self,instanceData):
        self.pyAAS.dataManager.pushInboundMessage({"functionType":1,"instanceid":self.instanceId,
                                                            "data":instanceData["data"],
                                                            "method":instanceData["method"]})
        vePool = True
        while(vePool):
            if (len(self.pyAAS.dataManager.outBoundProcessingDict.keys())!= 0):
                if (self.pyAAS.dataManager.outBoundProcessingDict[self.instanceId] != ""):
                    response = self.pyAAS.dataManager.outBoundProcessingDict[self.instanceId]
                    del self.pyAAS.dataManager.outBoundProcessingDict[self.instanceId]
                    vePool = False
        return response

class HTTPResponse(object):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def createExceptionResponse(self,send_Message):
        messageType = send_Message["frame"]["type"]
        smP = send_Message["frame"]["semanticProtocol"]["keys"][0]["value"]
        receiver = send_Message["frame"]["receiver"]["role"]["name"]
        I40FrameData = {
                                "semanticProtocol": smP,
                                "type" : messageType+"_"+str(self.pyAAS.dba.getMessageCount()["message"][0]+1),
                                "messageId" : "registerAck_1",
                                "SenderAASID" : self.pyAAS.AASID,
                                "SenderRolename" : "HTTP_ENDPoint",
                                "conversationId" : "AASNetworkedBidding",
                                "replyBy" :  "INTERNAL",
                                "replyTo" :  "INTERNAL",                                
                                "ReceiverAASID" :  self.pyAAS.AASID,
                                "ReceiverRolename" : receiver
                        }
        self.gen = Generic()
        self.frame = self.gen.createFrame(I40FrameData)
        
        self.InElem = self.pyAAS.dba.getAAsSubmodelsbyId(self.pyAAS.AASID,"StatusResponse")["message"][0]
        
        self.InElem["submodelElements"][0]["value"] = "E"
        self.InElem["submodelElements"][1]["value"] = "E009. delivery-error"
        self.InElem["submodelElements"][2]["value"] = "Unable to send the message to the target server"
         
        registerAckMessage ={"frame": self.frame,
                                "interactionElements":[self.InElem]}
        
       
                