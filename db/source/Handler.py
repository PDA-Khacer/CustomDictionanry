import os
import json

from db.source.Const import TABLE_NAME
from db.source.Const import MAX_RECORDS
from db.source.Const import HIGH_MODE
from db.source.Const import IS_HASH


class DBHandler:
    def __init__(self):
        self.__allTable = dict()
        self.__allFileData = []
        self.__cacheData = dict() 
        self.__keyData = []
        self.__keyIndex = dict() # map[int]string
        self.__tableCache = ""
        self.__currentIndex = -1
        self.__mode = 0

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
        self.__tableCache = table
        return self.__cacheData

    def writeItem(self, table, key, data):
        if type(key) != str:
            print(r'[ERR] db\source\Handler.py line:36 ',
                  "Key must be a string")
            return -1
        nameFile = self.selectFile(table)
        if table != self.__tableCache:
            self.readTable(table)
        if any(item == key for item in self.__keyData):
            print('key is existed')
            return -1

        try:
            f = open('db/data/'+nameFile, 'a')
            del nameFile
            if IS_HASH == 1:
                # f.write(self.__hash(
                #     "<" + str(self.__allTable[table] + 1) + "@" + str(key) + ":" + str(data) + ">"))
                f.write(self.__hash(self.itemToString(
                    str(self.__allTable[table] + 1), str(key), data)))
            else:
                # f.write("<" + str(self.__allTable[table] + 1) + "@" + str(key) + ":" + str(data) + ">")
                f.write(self.itemToString(
                    str(self.__allTable[table] + 1), str(key), data))
            self.__incTotalCount(table)
        except Exception as e:
            print(r'[ERR] Dir not exits')
            print(r'[ERR] db\source\Handler.py line:50 ', e)
        finally:
            f.close()

    def checkKeyExists(self, table, key):
        if type(key) != str:
            print(r'[ERR] db\source\Handler.py line:54 ',
                  "Key must be a string")
            return -1
        if table != self.__tableCache:
            self.readTable(table)
        if any(item == key for item in self.__keyData):
            print('key is existed')
            return True
        return False

    def getItem(self, table, key):
        """ Get item in table with key """
        if HIGH_MODE == self.__mode:
            # TODO: use thread
            pass
        else:
            self.readTable(table)
            try:
                self.__currentIndex = int(self.__cacheData[key]["index"])
                return self.__cacheData[key]
            except Exception as e:
                print(r'[ERR] no item in dict')
                return None

    def updateItem(self, table, key, value):
        if value == None:
            value = "{}"
        if HIGH_MODE == self.__mode:
            # TODO: use thread
            pass
        else:
            try:
                oldValue = self.getItem(table, key)['value']
            except Exception as e:
                print(r'[ERR] Item not existed !')
                print(r'[ERR] db\source\Handler.py line:98 ', e)
                return False
            nameFile = table+"_" + \
                str(self.__getNumberOfFile(self.__currentIndex))
            # replace
            newData = self.itemToString(self.__currentIndex, key, value)
            oldData = self.itemToString(self.__currentIndex, key, oldValue)
            newData = self.__readFile(nameFile).replace(oldData, newData)
            self.__reWriteFile(nameFile, newData)
        return True

    def deleteitem(self, table, key):
        if HIGH_MODE == self.__mode:
            # TODO: use thread
            pass
        else:
            try:
                oldValue = self.getItem(table, key)['value']
            except Exception as e:
                print(r'[ERR] Item not existed !')
                print(r'[ERR] db\source\Handler.py line:98 ', e)
                return False
            nameFile = table+"_" + \
                str(self.__getNumberOfFile(self.__currentIndex))
            oldData = self.itemToString(self.__currentIndex, key, oldValue)
            newData = self.__readFile(nameFile).replace(oldData, "")
            self.__reWriteFile(nameFile, newData)
            self.__descTotalCount(table)
        return True

    def itemToString(self, index, key, value):
        return '<{index}@{key}:{value}>'.format(index=index, key=str(key), value=json.dumps(value))

    def getItemByIndex(self, table, index):
        """ Get item in table with index """
        if HIGH_MODE == self.__mode:
            # TODO: use thread
            pass
        else:
            self.readTable(table)
            try:
                key = self.__keyIndex[index]
                return self.__cacheData[key]
            except Exception as e:
                print(r'[ERR] no item in dict')
                return None

    def updateItemByIndex(self, table, index, value):
        if value == None:
            value = "{}"
        if HIGH_MODE == self.__mode:
            # TODO: use thread
            pass
        else:
            try:
                oldValue = self.getItemByIndex(table, index)['value']
                key = self.__keyIndex[index]
            except Exception as e:
                print(r'[ERR] Item not existed !')
                print(r'[ERR] db\source\Handler.py line:98 ', e)
                return False
            nameFile = table+"_" + \
                str(self.__getNumberOfFile(self.__currentIndex))
            # replace
            newData = self.itemToString(self.__currentIndex, key, value)
            oldData = self.itemToString(self.__currentIndex, key, oldValue)
            newData = self.__readFile(nameFile).replace(oldData, newData)
            self.__reWriteFile(nameFile, newData)
        return True

    def deleteitemByIndex(self, table, index):
        if HIGH_MODE == self.__mode:
            # TODO: use thread
            pass
        else:
            try:
                oldValue = self.getItemByIndex(table, index)['value']
                key = self.__keyIndex[index]
            except Exception as e:
                print(r'[ERR] Item not existed !')
                print(r'[ERR] db\source\Handler.py line:98 ', e)
                return False
            nameFile = table+"_" + \
                str(self.__getNumberOfFile(self.__currentIndex))
            oldData = self.itemToString(self.__currentIndex, key, oldValue)
            newData = self.__readFile(nameFile).replace(oldData, "")
            self.__reWriteFile(nameFile, newData)
            self.__descTotalCount(table)
        return True

    # TODO: work with multiple data
    # TODO: get page data
    # TODO: clear all data
    # TODO: backup
    # TODO: trans
    # TODO: lock

    # private method

    def __readFileTables(self):
        try:
            f = open("db/data/" + TABLE_NAME, "r", encoding="utf-8")
            for line in f:
                line = line.replace('\n', '').split(' ')
                self.__allTable[line[0]] = int(line[2])
        except Exception as e:
            print(r'[ERR] IO Exception')
            print(r'[ERR] db\source\Handler.py line:27 ', e)
        finally:
            f.close()

    def __writeTableToFile(self, key):
        try:
            f = open("db/data/" + TABLE_NAME, "a", encoding="utf-8")
            f.writelines('\n' + str(key) + ' : 0')
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

    def __hash(self, string):
        re = ''
        for item in string:
            re += str(ord(item)+1234)
        return re

    def __hashData(self, index, key, value):
        re = ''
        for item in self.itemToString(index, key, value):
            re += str(ord(item)+1234)
        return re

    def __readFile(self, file):
        try:
            re = ""
            if IS_HASH == 1:
                with open('db/data/' + file, "rb") as f:
                    while (byte := f.read(4)):
                        re += str(chr(int(byte)-1234))
                    f.close()
            else:
                with open('db/data/' + file, "r") as f:
                    for line in f:
                        re += line
                    f.close()
        except Exception as e:
            print(r'[ERR] File not exit')
            print(r'[ERR] db\source\Handler.py line:195 ', e)
        return re

    def __reWriteFile(self, file, data):
        try:
            f = open('db/data/'+file, 'w')
            if IS_HASH == 1:
                f.write(self.__hash(data))
            else:
                f.write(data)
        except Exception as e:
            print(r'[ERR] file not existed !')
            print(r'[ERR] db\source\Handler.py line:96 ', e)
        finally:
            f.close()

    def __reWriteFileTable(self):
        try:
            f = open("db/data/" + TABLE_NAME, "w", encoding="utf-8")
            for key in self.__allTable:
                f.write(str(key) + ' : ' + str(self.__allTable[key]) + '\n')
        except Exception as e:
            print(r'[ERR] IO Exception')
            print(r'[ERR] db\source\Handler.py line:27 ', e)
        finally:
            f.close()

    def __toDict(self, string):
        # TODO: add function load cache
        self.__cacheData = dict()
        i = 0
        s = 1
        key = ""
        value = ""
        flag = -1
        while i < len(string):
            if string[i] == ':' and flag != 1:
                keyAndIndex = string[s:i].split("@")
                key = keyAndIndex[1]
                self.__currentIndex = int(keyAndIndex[0])
                self.__keyData.append(key)
                self.__keyIndex[int(keyAndIndex[0])]= key
                flag = 1
                s = i + 1
            if string[i] == ">":
                value = string[s:i]
                self.__cacheData[key] = dict(
                    index=keyAndIndex[0], value=json.loads(value))
                flag = -1
                s = i + 2
            i += 1

    def __incTotalCount(self, table):
        self.__readFileTables()
        self.__allTable[table] += 1
        self.__reWriteFileTable()

    def __descTotalCount(self, table):
        self.__readFileTables()
        self.__allTable[table] -= 1
        self.__reWriteFileTable()

    def debugData(self, table):
        pass

    def reIndex(self, table):
        self.readTable(table)
        allItem = dict(sorted(self.__cacheData.items(),
                       key=lambda item: item[1]['index']))
        stringData = ""
        index = 1
        for key, value in allItem.items():
            value['index'] = index
            allItem[key] = value
            stringData += self.itemToString(index=index,
                                            key=key, value=value['value'])
            if index % MAX_RECORDS == 0:
                print("rewrite file", table+"_"+str(int(index/MAX_RECORDS)))
                self.__reWriteFile(
                    table+"_"+str(int(index/MAX_RECORDS)), stringData)
                stringData = ''
            index += 1
        index -= 1
        if stringData != '':
            print("stringData", stringData)
            print("rewrite file", table+"_"+str(int(index/MAX_RECORDS) + 1))
            self.__reWriteFile(
                table+"_"+str(int(index/MAX_RECORDS) + 1), stringData)
        self.__allTable[table] = index
        self.__reWriteFileTable()
