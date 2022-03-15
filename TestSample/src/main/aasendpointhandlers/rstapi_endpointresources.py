'''
Copyright (c) 2021-2022 OVGU LIA
Author: Harish Kumar Pakala
This source code is licensed under the Apache License 2.0 (see LICENSE.txt).
This source code may use other Open Source software components (see LICENSE.txt).
'''
from flask_restful import Resource,request
from flask import render_template,Response,redirect,flash,make_response,session,send_file
from jsonschema import validate
from requests.utils import unquote

try:
    from utils.i40data import Generic
except ImportError:
    from main.utils.i40data import Generic

try:
    from utils.utils import ExecuteDBModifier,ProductionStepOrder,SubmodelUpdate,SubmodelElement,ExecuteDBRetriever,AASMetaModelValidator
except ImportError:
    from main.utils.utils import ExecuteDBModifier,ProductionStepOrder,SubmodelUpdate,SubmodelElement,ExecuteDBRetriever,AASMetaModelValidator
import os

class AAS(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def get(self,aasId):
        try:
            aasId = unquote(aasId)
            edbR = ExecuteDBRetriever(self.pyAAS)
            dataBaseResponse = edbR.execute({"data":{"updateData":"emptyData","aasId":aasId},"method":"getAASShellById"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except:
            return make_response("Unexpected Internal Server Error",500)
        
    def put(self,aasId):
        try:
            data = request.json
            aasId = unquote(aasId)
            if "interactionElements" in data:
                pass
                #return self.pyAAS.skillInstanceDict["AASHandler"].restAPIHandler(data)
            else: 
                aasValid = AASMetaModelValidator(self.pyAAS)           
                if(aasValid.validateAASShell(data)):
                    edm = ExecuteDBModifier(self.pyAAS)
                    dataBaseResponse = edm.executeModifer({"data":{"updateData":data,"aasId":aasId},"method":"putAASShellById"})
                    return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
                else :
                    return make_response("The syntax of the passed Asset Administration Shell is not valid or malformed request",400)
        except Exception as E:
            return make_response("Internal Server Error",500)

    def delete(self,aasId):
        try:
            aasId = unquote(aasId)
            edm = ExecuteDBModifier(self.pyAAS)
            dataBaseResponse = edm.executeModifer({"data":{"updateData":"empty","aasId":aasId},"method":"deleteAASShellById"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except Exception as E:
            return make_response("Unexpected Internal Server Error",500)


class AASassetInformation(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def get(self):
        try:
            edbR = ExecuteDBRetriever(self.pyAAS)
            dataBaseResponse = edbR.execute({"data":{"updateData":"emptyData"},"method":"getAssetInformation"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except:
            return make_response("Unexpected Internal Server Error",500)


class AASassetInformationById(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS

    def get(self,assetId):
        try:
            assetId = unquote(assetId)
            edbR = ExecuteDBRetriever(self.pyAAS)
            dataBaseResponse = edbR.execute({"data":{"updateData":"emptyData","assetId":assetId},"method":"getAASaasetInformationById"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except:
            return make_response("Unexpected Internal Server Error",500)
    
    def put(self,assetId):
        try:
            assetId = unquote(assetId)
            data = request.json
            if "interactionElements" in data: 
                pass
                #return self.pyAAS.skillInstanceDict["AASHandler"].restAPIHandler(data)
            else: 
                aasValid = AASMetaModelValidator(self.pyAAS)           
                if(aasValid.valitdateAsset(data)):
                    edm = ExecuteDBModifier(self.pyAAS)
                    dataBaseResponse = edm.executeModifer({"data":{"updateData":data,"assetId":assetId},"method":"putAASaasetInformationById"})
                    return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
                else :
                    return make_response("The syntax of the passed Asset Administration Shell is not valid or malformed request",400)
        except Exception as E:
            return make_response("Internal Server Error",500)

    def delete(self,aasetId):
        try:
            assetId = unquote(aasetId)
            edm = ExecuteDBModifier(self.pyAAS)
            dataBaseResponse = edm.executeModifer({"data":{"updateData":"empty","assetId":assetId},"method":"deleteAASaasetInformationById"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except Exception as E:
            return make_response("Unexpected Internal Server Error",500)

        
  
class AASsubmodelRefs(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def get(self,aasId):
        try:
            aasId = unquote(aasId)
            edbR = ExecuteDBRetriever(self.pyAAS)
            dataBaseResponse = edbR.execute({"data":{"updateData":"emptyData","aasId": aasId},"method":"getSubmodelRefsByAASId"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except:
            return make_response("Unexpected Internal Server Error",500)

class AASsubmodelRefsIndentifier(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS

    def get(self,aasId,submodelId):
        try:
            aasId = unquote(aasId)
            submodelId = unquote(submodelId)
            edbR = ExecuteDBRetriever(self.pyAAS)
            dataBaseResponse = edbR.execute({"data":{"updateData":"emptyData","aasId": aasId,"submodelId":submodelId},"method":"getSubmodelRefsByIDByAASId"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except:
            return make_response("Unexpected Internal Server Error",500)
      
    def put(self,aasId,submodelId):
        try:
            aasId = unquote(aasId)
            submodelId = unquote(submodelId)
            data = request.json
            if "interactionElements" in data:
                pass
                #return self.pyAAS.skillInstanceDict["AASHandler"].restAPIHandler(data)
            else:
                if(True):
                    if (True):
                        edm = ExecuteDBModifier(self.pyAAS)
                        dataBaseResponse = edm.executeModifer({"data":{"updateData":{"submodels":[data]},"aasId":aasId,"submodelId":submodelId},"method":"putSubmodelRefbyIdByAASId"})            
                        return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
                    else:
                        return make_response("The namspace SubmodelId value and the IdShort value do not match",500)
                else:
                    return make_response("The syntax of the passed submodel data is not valid or malformed request",400)
        except Exception as E:
            return make_response("Unexpected Internal Server Error",500)

    def delete(self,aasId,submodelId):
        try:
            aasId = unquote(aasId)
            submodelId = unquote(submodelId)
            edm = ExecuteDBModifier(self.pyAAS)
            dataBaseResponse = edm.executeModifer({"data":{"updateData":"empty","aasId":aasId,"submodelId":submodelId},"method":"deleteSubmodelRefbyIdByAASId"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except Exception as E:
            return make_response("Unexpected Internal Server Error",500)
#
class Submodels(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def get(self):
        try:
            edbR = ExecuteDBRetriever(self.pyAAS)
            dataBaseResponse = edbR.execute({"data":{"updateData":"emptyData"},"method":"getSubmodels"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except:
            return make_response("Unexpected Internal Server Error",500)

class SubmodelsById(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
        
    def get(self,submodelId):
        try:
            submodelId = unquote(submodelId)
            edbR = ExecuteDBRetriever(self.pyAAS)
            dataBaseResponse = edbR.execute({"data":{"updateData":"emptyData","submodelId":submodelId},"method":"getSubmodelById"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except:
            return make_response("Unexpected Internal Server Error",500)
        
    def put(self,submodelId):
        try:
            aasValid = AASMetaModelValidator(self.pyAAS)
            submodelId = unquote(submodelId)
            data = request.json
            if "interactionElements" in data:
                pass
                #return self.pyAAS.skillInstanceDict["AASHandler"].restAPIHandler(data)
            else:
                if(aasValid.valitdateSubmodel({"submodels":[data]})):
                    if (True):
                        edm = ExecuteDBModifier(self.pyAAS)
                        dataBaseResponse = edm.executeModifer({"data":{"updateData":{"submodels":[data]},"submodelId":submodelId},"method":"putSubmodelById"})            
                        return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
                    else:
                        return make_response("The namspace SubmodelId value and the IdShort value do not match",500)
                else:
                    return make_response("The syntax of the passed submodel data is not valid or malformed request",400)
        except Exception as E:
            return make_response("Unexpected Internal Server Error",500)

    def delete(self,submodelId):
        try:
            edm = ExecuteDBModifier(self.pyAAS)
            submodelId = unquote(submodelId)
            dataBaseResponse = edm.executeModifer({"data":{"updateData":"empty","submodelId":submodelId},"method":"deleteSubmodelById"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except Exception as E:
            return make_response("Unexpected Internal Server Error",500)

   

class SubmodelElemsById(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def get(self,submodelId):
        try:
            submodelId = unquote(submodelId)
            edbR = ExecuteDBRetriever(self.pyAAS)
            dataBaseResponse = edbR.execute({"data":{"updateData":"emptyData","submodelId": submodelId},"method":"getSubmodeByIdlElements"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except Exception as E:
            return make_response("Unexpected Internal Server Error",500)

class SubmodelElementsByPath(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
        
    def get(self,submodelId,idShortPath):
        try:
            submodelId = unquote(submodelId)
            edbR = ExecuteDBRetriever(self.pyAAS)
            dataBaseResponse = edbR.execute({"data":{"updateData":"emptyData","submodelId":submodelId,"idShortPath":idShortPath},"method":"getSubmodelByIdElementByIdShortPath"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except:
            return make_response("Unexpected Internal Server Error",500)

    def put(self,submodelId,idShortPath):
        try:
            data = request.json 
            submodelId = unquote(submodelId)
            edm = ExecuteDBModifier(self.pyAAS)
            dataBaseResponse = edm.executeModifer({"data":{"updateData":data,"submodelId":submodelId,"idShortPath":idShortPath},"method":"putSubmodelByIdElementByIdShortPathValue"})
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except Exception as E:
            return make_response("Internal Server Error",500)


class SubmodelElementsByPathValue(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
        
    def get(self,submodelId,idShortPath):
        try:
            submodelId = unquote(submodelId)
            edbR = ExecuteDBRetriever(self.pyAAS)
            dataBaseResponse = edbR.execute({"data":{"updateData":"emptyData","submodelId":submodelId,"idShortPath":idShortPath},"method":"getSubmodelByIdElementByIdShortPathValue"})            
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except Exception as E:
            return make_response("Unexpected Internal Server Error",500)

    def put(self,submodelId,idShortPath):
        try:
            data = request.json
            submodelId = unquote(submodelId)
            edm = ExecuteDBModifier(self.pyAAS)
            dataBaseResponse = edm.executeModifer({"data":{"updateData":data,"submodelId":submodelId,"idShortPath":idShortPath},"method":"putSubmodelByIdElementByIdShortPathValue"})
            return make_response(dataBaseResponse["message"][0],dataBaseResponse["status"])
        except Exception as E:
            return make_response("Internal Server Error",500)


class RetrieveMessage(Resource):    
    def __init__(self, pyAAS):
        self.pyAAS = pyAAS
        
    def post(self):
        jsonMessage = request.json
        try:
            if (jsonMessage["frame"]["sender"]["identification"]["id"] == self.pyAAS.AASID):
                pass
            else:
                self.pyAAS.msgHandler.putIbMessage(jsonMessage)
        except:
            pass

class AASWebInterface(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS

    def get(self,aasId):
        if not session.get('logged_in'):
            return redirect("/login")
        else:              
            try:
                return  Response(render_template('index.html',aasId=aasId,skillList= self.pyAAS.skillListWeb[aasId],namePlateData = self.pyAAS.namePlateData[aasId]))
            except Exception as E:
                return str(E)


class AASWebInterfaceDocumentation(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS

    def get(self,aasId):
        if not session.get('logged_in'):
            return redirect("/login")
        else:              
            try:
                return  Response(render_template('documentation.html',aasId=aasId,skillList= self.pyAAS.skillListWeb[aasId],documentList = self.pyAAS.documentationData[aasId], namePlateData = str(self.pyAAS.namePlateData[aasId])))
            except Exception as E:
                return str(E)

class AASWebInterfaceHome(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS

    def get(self):
        if not session.get('logged_in'):
            return redirect("/login")
        else:              
            try:
                return  Response(render_template('home.html',aasList = self.pyAAS.AASData))
            except Exception as E:
                return str(E)
            
            

class AASWebInterfaceBoringRequester(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def post(self,aasId):
        try:
            updateInfo = request.form
            tabType = updateInfo["tabType"]
            if (tabType == "status"):
                try:
                    return redirect("BoringRequester")
                except Exception as e:
                    flash("Error" + str(e),"info")
                    return redirect("BoringRequester")
        except Exception as e:
            return self.pyAAS.msgHandler.BoringRequesterLogList.getCotent()
        
    def get(self,aasId):
        if not session.get('logged_in'):
            return redirect("/login")
        else:           
            return  Response(render_template('BoringRequester.html',aasId=aasId,skillList= self.pyAAS.skillListWeb[aasId]))

class AASWebInterfaceTransportRequester(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def post(self,aasId):
        try:
            updateInfo = request.form
            tabType = updateInfo["tabType"]
            if (tabType == "status"):
                try:
                    return redirect("TransportRequester")
                except Exception as e:
                    flash("Error" + str(e),"info")
                    return redirect("TransportRequester")
        except Exception as e:
            return self.pyAAS.msgHandler.TransportRequesterLogList.getCotent()
    def get(self,aasId):
        if not session.get('logged_in'):
            return redirect("/login")
        else:           
            return  Response(render_template('TransportRequester.html',aasId=aasId,skillList= self.pyAAS.skillListWeb[aasId]))

class AASWebInterfaceHoningRequester(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def post(self,aasId):
        try:
            updateInfo = request.form
            tabType = updateInfo["tabType"]
            if (tabType == "status"):
                try:
                    return redirect("HoningRequester")
                except Exception as e:
                    flash("Error" + str(e),"info")
                    return redirect("HoningRequester")
        except Exception as e:
            return self.pyAAS.msgHandler.HoningRequesterLogList.getCotent()
    def get(self,aasId):
        if not session.get('logged_in'):
            return redirect("/login")
        else:           
            return  Response(render_template('HoningRequester.html',aasId=aasId,skillList= self.pyAAS.skillListWeb[aasId]))


class AASWebInterfaceSubmodels(Resource):
    
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS

    def get(self,aasId):
        if not session.get('logged_in'):
            return redirect("/login")
        else:          
            try:
                return  Response(render_template('submodels.html', namePlateData = self.pyAAS.namePlateData[aasId], skillList= self.pyAAS.skillListWeb[aasId], propertyListDict=(self.pyAAS.getSubmodelPropertyListDict(aasId))))
            except Exception as e:
                return str(e)
        
    def post(self,aasId):
        try:
            updateInfo = request.form
            self.pyAAS.serviceLogger.info(updateInfo)
            methodType = updateInfo["methodType"]
            submodelName = updateInfo["submodelName"]
            if methodType == "modify" :
                propertyName = updateInfo["propertyName"]
                newValue = updateInfo["newValue"]
                if newValue != "":
                    sUpdate = SubmodelUpdate(self.pyAAS)
                    modifyResponse = sUpdate.modify(submodelName,propertyName,newValue)
                    if (modifyResponse["status"] == 500):
                        flash("Internal Data Error","error")
                        return redirect("submodels")
                    else:
                        flash("Data updated succesfully","info")
                        return redirect("submodels")
                else:
                    flash("Empty data field cannot be updated","error")
                    return redirect("submodels")
                
            elif (methodType == "delete"):
                propertyName = updateInfo["propertyName"]
                sUpdate = SubmodelUpdate(self.pyAAS)
                modifyResponse = sUpdate.delete(propertyName,submodelName)
                if (modifyResponse["status"] == 500):
                    flash("Internal Data Error","error")
                    return redirect("submodels")
                else:
                    flash("Data updated succesfully","info")
                    return redirect("submodels")
        except Exception as e:
            flash(str(e),"error")
            return redirect("submodels")

class AASWebInterfaceSubmodelProperty1(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def post(self):
        try:
            updateInfo = request.form
            IdShort =  updateInfo["IdShort"]
            Value = updateInfo["Value"]
            SemanticId = updateInfo["SemanticId"]
            submodelId = updateInfo["property"]
            
            if (IdShort == "" or Value == "" or  SemanticId == ""):
                flash("Please fill all the fields","error")
                return redirect("/submodels")
            else:
                submodeElement = SubmodelElement(IdShort,Value,SemanticId,self.pyAAS)
                submodelElem = submodeElement.create()
                returnmessage = submodeElement.addSubmodelElement(submodelElem,submodelId)
                if (returnmessage["status"] == 200):
                    subUpdate = SubmodelUpdate(self.pyAAS)
                    returnMessage = subUpdate.update(returnmessage["message"],submodelId)
                    print(returnMessage)
                    if (returnMessage["status"] == 200):
                        flash("Details updated Succesfully"+returnMessage["message"][0],"success")
                        return redirect("/submodels")
                    else:
                        flash("Internal error"+returnMessage["message"][0],"error")
                        return redirect("/submodels")
                else:
                    flash("Internal error"+returnMessage["message"][0],"error")
                    return redirect("/submodels")
        except Exception as E:
            return str(E)
      

class AASWebInterfaceLog(Resource):
    
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS

    def get(self):
        if not session.get('logged_in'):
            return redirect("/login")
        else:          
            return  Response(render_template('systemlog.html',namePlateData = self.pyAAS.namePlateData,skillList= self.pyAAS.skillListWeb))

    def post (self):
        return self.pyAAS.ServiceLogList.getCotent()

class AASWebInterfaceSKillLog(Resource):
    
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS

    def get(self,SkillName,aasIdentifier):
        if not session.get('logged_in'):
            return redirect("/login")
        else:          
            return self.pyAAS.msgHandler.logListDict[aasIdentifier][SkillName].getCotent()

class AASWebInterfaceSearch(Resource):
    
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def post(self,aasIdentifier):
        try:
            updateInfo = request.form
            query =  updateInfo["search"]
            message1 = self.pyAAS.dba.getConversationsById(query)
            if message1["status"] == 200:
                messages = self.pyAAS.dba.getConversationsById(query)["message"]
                return  Response(render_template('search.html',skillList= self.pyAAS.skillListWeb[aasIdentifier],resultList = {query:messages}))
            else:
                count = self.pyAAS.dba.getMessageCount()
                flash("The conversation Id is not found, the last count is " + str(count["message"][0]),"error")
                return redirect("/")
                
        except Exception as e:
            flash("Error","error")
            return redirect("/")

class AASWebInterfaceSearchbyId(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def get(self,query):
        if not session.get('logged_in'):
            return redirect("/login")
        else:          
            try:
                queryList = str(unquote(query)).split("**")
                return self.pyAAS.dba.getMessagebyId(queryList[0],queryList[1])["message"][0]
            except Exception as e:
                print(str(queryList) + str(e))
                return str(queryList) + str(e)

class AASWebInterfaceProductionManagement(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS

    def get(self,aasId):   
        if not session.get('logged_in'):
            return redirect("/login")
        else:          
            try:
                return Response(render_template('productionmanager.html',aasId=aasId,namePlateData = self.pyAAS.namePlateData[aasId],productionStepList=self.pyAAS.productionStepList,conversationIdList=self.pyAAS.conversationIdList,productionSequenceList=self.pyAAS.productionSequenceList[aasId],skillList= self.pyAAS.skillListWeb[aasId] ))
            except Exception as e:
                return str(e)

    def post(self,aasIdentifier):
        updateInfo = request.form
        tag =  updateInfo["operationType"]   
        
        if (tag =="home"):
            return redirect("/productionmanger")
        
        elif (tag == "create"):
            productionStep = request.form.get("productionStep")
            self.pyAAS.productionSequenceList.append(productionStep)
            flash("New Production step is added","success")
            return redirect("/productionmanger")
        
        elif (tag == "delete"):
            self.pyAAS.productionSequenceList = []
            flash("New Production step is added","success")
            return redirect("/productionmanger")
        
        elif (tag == "start"):
            try:
                pso = ProductionStepOrder(self.pyAAS)
                conversationID = pso.createProductionStepOrder()
                flash("New Order booked with Order ID " + conversationID + " is booked","info")
                return redirect("/productionmanger")       
            except  Exception as e:
                flash("Error creating the conversation Id.","error")
                return redirect("/productionmanger")

class AASWebInterfaceRegister(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS

    def post(self,aasIdentifier):
        try:
            updateInfo = request.form
            tabType = updateInfo["tabType"]
            if (tabType == "status"):
                try:
                    return redirect("register")
                except Exception as e:
                    flash("Error" + str(e),"info")
                    return redirect("register")
        except Exception as e:
            return self.pyAAS.msgHandler.RegisterLogList.getCotent()
    

    def get(self,aasIdentifier):
        if not session.get('logged_in'):
            return redirect("/login")
        else:          
            return  Response(render_template('register.html',namePlateData = self.pyAAS.namePlateData[aasIdentifier],skillList= self.pyAAS.skillListWeb[aasIdentifier]))

class AASWebInterfaceSubmodelProperty(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
                
    def performDBUpdate(self,updateValue,submodelName,submodelProperty):
        try:
            edm = ExecuteDBModifier(self.pyAAS)
            dataBaseResponse = edm.executeModifer({"data":{"updateData":{"value":updateValue},"aasId":self.pyAAS.AASID,"submodelId":submodelName,"propertyId":submodelProperty},"method":"putSubmodelPropertyValuebyId"})              
        except Exception as E:
            print(str(E)) 

    def post(self):
        updateData = request.form
        submodelName = updateData["submodelName"]
        submodelProperty = updateData["submodelProperty"] 
        updateValue = updateData["newValue"]  
        self.performDBUpdate(updateValue,submodelName,submodelProperty)
        if (submodelName == "Nameplate"):
            return redirect("/")
        else :
            return redirect("/submodels")
        

class AASDocumentationDownload(Resource):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
    
    def post(self,filename):
        try:
            file_path = os.path.join(self.pyAAS.downlaod_repository,filename)
            sendfile = send_file(file_path,attachment_filename=filename, as_attachment=True,mimetype= "application/pdf")
            print(sendfile)
            return  sendfile
        except Exception as E:
            print(str(E))
        