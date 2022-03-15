'''
Copyright (c) 2021-2022 Otto-von-Guericke-Universiat Magdeburg, Lehrstuhl Integrierte Automation
Author: Harish Kumar Pakala
This source code is licensed under the Apache License 2.0 (see LICENSE.txt).
This source code may use other Open Source software components (see LICENSE.txt).
'''

class AAS_Database_Server(object):
    def __init__(self,pyAAS):
        self.pyAAS = pyAAS
        self.AASRegistryDatabase = self.pyAAS.aasConfigurer.dataBaseFile
    
    def createNewDataBaseColumn(self,colName):
        if colName in self.AASRegistryDatabase:
            return colName
        else:
            self.AASRegistryDatabase[colName] =  []
            return colName
    
    def checkforExistenceofColumn(self,colName):
        if colName in self.AASRegistryDatabase:
            if self.AASRegistryDatabase[colName] == []:
                return "empty column"
            else:
                return "data present"
        else:
            return "column not present"
        
    def insert_one(self,colName,insertData):
        self.AASRegistryDatabase[colName].append(insertData)
        return self.pyAAS.aasConfigurer.saveToDatabase(self.AASRegistryDatabase)

    def delete_one(self,colName):
        self.AASRegistryDatabase[colName] = []
        return self.pyAAS.aasConfigurer.saveToDatabase(self.AASRegistryDatabase)    
     
        