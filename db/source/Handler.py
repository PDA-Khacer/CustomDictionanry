import os

from db.source.Const import TABLE_NAME
from db.source.Const import MAX_RECORDS

class DBHandler:
    def __init__(self):
        self.__allTable = dict()
        self.__allFileData = []

    def selectFile(self, key1):
        self.__readFileTables()
        print(self.__allTable)
        if key1 in self.__allTable:
            self.__getAllFileData()
            return key1 + '_' + str(self.__getNumberOfFile(self.__allTable[key1]))
        else:
            self.__writeTableToFile(key1)
            return key1 + "_1"
        
    # private method
    def __readFileTables(self):
        try:
            f = open("db/data/" + TABLE_NAME, "r", encoding="utf-8")
            for line in f:
                line = line.replace('\n', '').split(' ')
                self.__allTable[line[0]] = line[2]
        except Exception as e:
            print(r'[ERR] IO Exception')
            print(r'[ERR] db\source\Handler.py line:27 ', e)
        finally:
            f.close()
        
    def __writeTableToFile(self, key):
        try:
            f = open("db/data/" + TABLE_NAME, "a", encoding="utf-8")
            f.writelines('\n'+ key + ' : 0')
        except Exception as e:
            print(r'[ERR] IO Exception')
            print(r'[ERR] db\source\Handler.py line:37 ', e)
        finally:
            f.close()

    def __getAllFileData(self):
        self.__allFileData = os.listdir('db/data')
    
    def __getNumberOfFile(self, totalCount):
        try:
            return int(int(totalCount) / MAX_RECORDS) + 1
        except Exception as e:
            print(r'[ERR] total count not int format')
            print(r'[ERR] db\source\Handler.py line:52 ', e)
            return -1