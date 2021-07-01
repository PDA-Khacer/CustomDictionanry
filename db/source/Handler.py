import os

from db.source.Const import TABLE_NAME
from db.source.Const import MAX_RECORDS


class DBHandler:
    def __init__(self):
        self.__allTable = dict()
        self.__allFileData = []
        self.__cacheData = dict()
        self.__keyData = []

    def selectFile(self, key1):
        self.__readFileTables()
        print(self.__allTable)
        if key1 in self.__allTable:
            self.__getAllFileData()
            return key1 + '_' + str(self.__getNumberOfFile(self.__allTable[key1]))
        else:
            self.__writeTableToFile(key1)
            return key1 + "_1"

    def readTable(self, table):
        self.__getAllFileData()
        for file in self.__allFileData:
            if table in file:
                dataFile = self.__readFile(file)
                self.__toDict(dataFile)
        return self.__cacheData

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
            f.writelines('\n' + key + ' : 0')
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

    def writeItem(self, table, key, data):
        nameFile = self.selectFile(table)
        try:
            f = open('db/data/'+nameFile, 'a')
            f.write(self.__hash("<" + str(key) + ":" + str(data) + ">"))
        except Exception as e:
            print(r'[ERR] Dir not exits')
            print(r'[ERR] db\source\Handler.py line:62 ', e)

    def __hash(self, string):
        re = ''
        for item in string:
            re += str(ord(item)+1234)
        return re

    def __readFile(self, file):
        try:
            re = ""
            with open('db/data/' + file, "rb") as f:
                while (byte := f.read(4)):
                    re += str(chr(int(byte)-1234))
                f.close()
        except Exception as e:
            print(r'[ERR] File not exit')
        return re

    def __toDict(self, string):
        i = 0
        s = 1
        key = ""
        value = ""
        flag = -1
        while i < len(string):
            if string[i] == ':' and flag != 1:
                key = string[s:i]
                self.__keyData.append(key)
                flag = 1
                s = i + 1
            if string[i] == ">":
                value = string[s:i]
                self.__cacheData[key] = value
                flag = -1
                s = i + 2
            i += 1
