from tkinter import *
from tkinter import messagebox as mb
from datetime import datetime
import _thread
import time

from db.source import Handler as DB


class GUIEditTopic:
    def __init__(self, DB, index=None):
        self._mainWindow = Tk()
        self._mainWindow.eval('tk::PlaceWindow . center')
        self._mainWindow.protocol("WM_DELETE_WINDOW", self.__on_closing())
        self.__DB = DB
        self._row = None
        Data = None
        # var

        # components
        if index != None:
            Data = DB.getItemByIndex("topic", index)
            self._row = Data
        Stt = Data == None and " " or Data['index']
        Name = Data == None and " " or Data['value']['Name']
        self.__label_Stt = Label(self._mainWindow, text="NO.",font=('Helvetica', 12, 'bold'))
        self.__entry_Stt = Entry(self._mainWindow, width=20,font=('Helvetica', 12))
        self.__entry_Stt.insert(END, Stt)
        self.__entry_Stt.config(state='readonly')
        self.__label_Name = Label(self._mainWindow, text="Name",font=('Helvetica', 12, 'bold'))
        self.__entry_Name = Entry(self._mainWindow, width=20,font=('Helvetica', 12))
        self.__entry_Name.insert(END, Name)
        self.__btn_save = Button(self._mainWindow, text="Save", font=('Helvetica', 15), command=self.__save_info)
        self.__label_Stt.grid(row=0, column=0, padx=10)
        self.__entry_Stt.grid(row=0, column=1)
        self.__label_Name.grid(row=1, column=0, padx=10)
        self.__entry_Name.grid(row=1,column=1)
        self.__btn_save.grid(row=2,column=0, columnspan= 2, sticky=N)
        # grid
        self._mainWindow.grab_set()

    def __on_closing(self):
        self._mainWindow.grab_release()

    def __save_info(self):
        if self._row != None:
            self._row['value']['Name'] = str(self.__entry_Name.get())
            self._row['value']['UpdateAt'] = str(datetime.now())
            self.__DB.updateItemByIndex("topic", int(self._row['index']), self._row['value'])
        else:
            item = dict(Name="develop", CreateAt=str(datetime.now()), CreateBy='admin', UpdateAt=str(datetime.now()))
            item['Name'] = str(self.__entry_Name.get()).strip()
            self.__DB.writeItem("topic", item['Name'], item)
        self._mainWindow.grab_release()
        self._mainWindow.destroy()

    def Render(self):
        try:
            self._mainWindow.mainloop()
        except Exception as e:
            print(r'[ERR] not init components !')
            print(r'[ERR] gui\login.py line:52 ', e)
