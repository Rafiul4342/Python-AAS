'''
Created on 24 Oct 2021

@author: pakala
'''
try:
    from utils.utils import ExecuteDBModifier
except ImportError:
    from main.utils.utils import ExecuteDBModifier

def function(pyAAS, *args):
    propertyName = args["propertyName"]
    idShortPath = args["idShortPath"]
    accessURI = args["href"]
    if (accessURI[0:8] == "opc.tcp:"):
        newValue = pyAAS.assetaccessEndpointHandlers["OPCUA"].read()
        edm = ExecuteDBModifier(pyAAS)
        dataBaseResponse = edm.executeModifer({"data":{"updateData":{"value",newValue},"aasId":pyAAS.AASID,"idShort":idShortPath},"method":"putSubmodelElementQualbyId"})            
        