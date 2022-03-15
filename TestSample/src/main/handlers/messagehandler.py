
'''
Copyright (c) 2021-2022 OVGU LIA
Author: Harish Kumar Pakala
This source code is licensed under the Apache License 2.0 (see LICENSE.txt).
This source code may use other Open Source software components (see LICENSE.txt).
'''

import  threading
import time
import uuid

try:
    import queue as Queue
except ImportError:
    import Queue as Queue 

try:
    from datastore.datamanager import DataManager
except ImportError:
    from main.datastore.datamanager import DataManager

try:
    from utils.aaslog import serviceLogHandler,LogList
except ImportError:
    from main.utils.aaslog import serviceLogHandler,LogList
try:
    from utils.i40data import Generic
except ImportError:
    from main.utils.i40data import Generic    


class MessageHandler(object):
    '''
    classdocs
    '''

    def __init__(self, pyAAS):
        '''
        Constructor
        '''
        self.pyAAS = pyAAS
        self.inBoundQueue = Queue.Queue()
        self.outBoundQueue = Queue.Queue()
        self.statusMessageQueue = Queue.Queue()
        self.assetDataValuesQueue = Queue.Queue()
        
        self.BoringRequesterLogList = LogList()
        self.BoringRequesterLogList.setMaxSize(maxSize= 200)
        self.TransportRequesterLogList = LogList()
        self.TransportRequesterLogList.setMaxSize(maxSize= 200)
        self.HoningRequesterLogList = LogList()
        self.HoningRequesterLogList.setMaxSize(maxSize= 200)
          
        self.ProductionManagerLogList = LogList()
        self.ProductionManagerLogList.setMaxSize(maxSize= 200)
        
        self.RegisterLogList = LogList()
        self.RegisterLogList.setMaxSize(maxSize= 200)      
        
        self.logListDict = {
                            "ProductionManager":self.ProductionManagerLogList,
                              "BoringRequester":self.BoringRequesterLogList,
                              "TransportRequester":self.TransportRequesterLogList,
                              "HoningRequester":self.HoningRequesterLogList,
                            "Register":self.RegisterLogList
                            }
        
        self.assetBatchCount = 1
        self.POLL = True
        
    def start(self, skillName, AASendPointHandlerObjects):
        self.skillName = skillName
        self.AASendPointHandlerObjects = AASendPointHandlerObjects
        bCount = 0
                
        while self.POLL:
            time.sleep(0.01)
            if (self.outBoundQueue).qsize() != 0:
                obThread = threading.Thread(target=self.sendOutBoundMessage, args=(self.getObMessage(),))     
                obThread.start()
            if (self.inBoundQueue).qsize() != 0:
                ibThread = threading.Thread(target=self._receiveMessage_, args=(self.getIbMessage(),))     
                ibThread.start()
            if (self.statusMessageQueue).qsize() != 0:
                smThread = threading.Thread(target=self.sendObstatusMessage, args=(self.getstatusMessage(),))
                smThread.start()
            if (self.assetDataValuesQueue).qsize() != 0:
                if (self.assetBatchCount == bCount + 1):
                    bCount = self.assetBatchCount
                    assetBatchThread = threading.Thread(target=self.processAssetDataValueBatch)
                    #assetBatchThread.start()
            
    def stop(self):
        
        self.POLL = False
        
    def putIbMessage(self, message):
        self.inBoundQueue.put((message))
    
    def getIbMessage(self):
        return self.inBoundQueue.get()
    
    def putObMessage(self, message):
        self.outBoundQueue.put(message)
    
    def getObMessage(self):
        return self.outBoundQueue.get()
    
    def getstatusMessage(self):
        return self.statusMessageQueue.get()
    
    def putStatusMessage(self, sMessage):
        self.statusMessageQueue.put(sMessage)
    
    def processMessage(self):
        self.getMessage()
        
    def assigntoSkill(self, _skillName):
        return self.skillName[_skillName]
    
    def createNewUUID(self):
        return uuid.uuid4()
        
    def _receiveMessage_(self, jMessage):
        try:
            _skillName = jMessage["frame"]["receiver"]["role"]["name"]
            self.assigntoSkill(_skillName).receiveMessage(jMessage)
        except:
            for skillName in self.skillName.keys():
                self.assigntoSkill(skillName).receiveMessage(jMessage)

    def sendOutBoundMessage(self, ob_Message):
        try:
            adaptorType = ob_Message["frame"]["replyTo"]
            if adaptorType == "MQTT":
                self.AASendPointHandlerObjects["MQTT"].dispatchMessage(ob_Message)
            elif adaptorType == "RESTAPI":
                self.AASendPointHandlerObjects["RESTAPI"].dispatchMessage(ob_Message)
            elif adaptorType == "Internal":
                self.putIbMessage(ob_Message)
            else:
                pass           
        except Exception as E:
            self.putIbMessage(ob_Message)
            
    def sendObstatusMessage(self, sMessage):
        pass
    
    def putAssetMessage(self, message):
        self.assetDataValuesQueue.put(message)
    
    def getAssetMessage(self):
        return self.assetDataValuesQueue.get()
    
    def processAssetDataValueBatch(self):
        time.sleep(5)
        assetQueueSize = self.assetDataValuesQueue.qsize()
        newAssetValueBatch = []
        for i in range (0, assetQueueSize):
            newAssetValueBatch.append(self.getAssetMessage())
        self.assetBatchCount = self.assetBatchCount + 1
        self.pyAAS.dataStoreManager.assetDataStoreBackup()
        self.pyAAS.dataStoreManager.assetDataValueStore(newAssetValueBatch)
        
    def trigggerHeartBeat(self):
        hbt = Generic()
        heartBeatCount = 1
        while True:
            _hbtMessage = hbt.createHeartBeatMessage(self.pyAAS.AASID,heartBeatCount)
            if (self.pyAAS.lia_env_variable["LIA_PREFEREDI40ENDPOINT"] == "MQTT"):
                self.AASendPointHandlerObjects["MQTT"].dispatchMessage(_hbtMessage)
            else:
                self.AASendPointHandlerObjects["RESTAPI"].dispatchMessage(_hbtMessage)
            time.sleep(5)
            heartBeatCount = heartBeatCount + 1
