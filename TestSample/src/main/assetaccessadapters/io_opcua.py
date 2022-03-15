# This is a demo IOAdapter

from opcua import Client

try:
    from abstract.assetendpointhandler import AsssetEndPointHandler
except ImportError:
    from main.abstract.assetendpointhandler import AsssetEndPointHandler


class AsssetEndPointHandler(AsssetEndPointHandler):

    def __init__(self, pyAAS):
        self.pyAAS = pyAAS


    def tdRead(self,urI):
        host = urI.split("opc.tcp://")[1].split("/")[0].split(":")
        IP = host[0]
        PORT = host[1]
        nodeId = urI.split("opc.tcp://")[1].split("/")[1]
        self.td_opcua_client = Client("opc.tcp://" + IP + ":" + PORT + "/")
        MW_VALUE = 0
        try:
            self.td_opcua_client.connect() 
            MW_VALUE = self.td_opcua_client.get_node(nodeId).get_value()
        except Exception as e:
            print(e)
            self.td_opcua_client.disconnect()
            MW_VALUE = 1 
        finally:
            self.td_opcua_client.disconnect()
            return MW_VALUE

    def tdWrite(self,urI,value):
        host = urI.split("opc.tcp://")[1].split("/")[0].split(":")
        IP = host[0]
        PORT = host[1]
        nodeId = urI.split("opc.tcp://")[1].split("/")[1]
        self.td_opcua_client = Client("opc.tcp://" + IP + ":" + PORT + "/")
        MW_VALUE = 0
        try:
            self.td_opcua_client.connect() 
            tdProperty = self.td_opcua_client.get_node(nodeId)
            tdProperty.set_value(value)
        except Exception as e:
            print(e)
            self.td_opcua_client.disconnect()
            MW_VALUE = 1 
        finally:
            self.td_opcua_client.disconnect()
            return MW_VALUE
        