from tkinter import *
from tkinter import messagebox as mb
from datetime import datetime
import _thread
import time

from db.source import Handler as DB
from design import editView as GUIEdit

MAX_ROW_ONE_VIEW = 15

class GUIListTopic:
    def __init__(self):
        str_footer = "Total count: {count}        Now: {time}     Who: {name}"
        self._numbeCol = 4
        nameTable = ["No.", "Name", "CreateAt", "CreateBy"]
        self._widthCols = [5,20,25,15]
        self._beginRow = 0
        self._mainWindow = Tk()
        # self._mainWindow.eval('tk::PlaceWindow . center')
        self._isEdit = False
        self._isDetail = False
        # self._mainWindow.geometry('640x550')
        self.__dbIns = DB.DBHandler()
        self._container = Frame(self._mainWindow,bg="white")
        self._container.grid(sticky=NS, columnspan=6) 
    
        self._string_topic = "All Topic"
        for i in range(len(nameTable)+2):
            # self.e = Entry(self._mainWindow, width=20, fg='black',font=('Arial', 14, 'bold'))
            e = Label(self._container, text=' ',bg="white")
            e.grid(row=self._beginRow, column=i, columnspan=1,padx=0,sticky=NW)
        self._label_all_topic = Label(self._container, text=self._string_topic, font='Helvetica 17 bold', justify=CENTER,bg="white")
        
        # self._first_col.grid(row=self._beginRow, column=0, sticky=N, pady=0, padx=0)
        # self._final_col.grid(row=self._beginRow, column=1 + len(nameTable), sticky=N, pady=0, padx=0)
        self._label_all_topic.grid(row=self._beginRow+1, column=0, columnspan=5, sticky=N, pady=15) 
        
        self.FrameWithScroll()
        
        # header table    
        for i in range(len(nameTable)):
            # self.e = Entry(self._mainWindow, width=20, fg='black',font=('Arial', 14, 'bold'))
            self.e = Entry(self._container, width=self._widthCols[i], fg='black',font=('Helvetica', 12, 'bold') ,justify='center')
            self.e.grid(row=self._beginRow+2, column=i+1, columnspan=1,padx=0,sticky=NW)
            self.e.insert(END, nameTable[i])
            self.e.config(state="readonly")
        self._search_entry = Entry(self._container, width=30,fg='black',font=('Helvetica', 12, 'bold'))
        self._search_entry.grid(row=self._beginRow+2, column=6, columnspan=2,padx=0,sticky=NW)
        self._btn_search = Button(self._container, text=chr(0x0001F50D),width=3, height=1, font="Helvetica 12", anchor=N, bg="lightgray")
        self._btn_search.grid(row=self._beginRow+2, column=7, columnspan=1,padx=0,sticky=NW)
        self._detail = Text(self._container, height=20, width=50)
        self._scroll_detail_text = Scrollbar(self._container, command=self._detail.yview)
        self._detail.configure(yscrollcommand=self._scroll_detail_text.set)
        self._detail.grid(column=len(nameTable)+2, row=self._beginRow+3)
        self._scroll_detail_text.grid(column=len(nameTable)+3, row=self._beginRow+3, sticky='ns')
        # content table
        self.ReloadData()
        
        # footer
        widthFooter = sum([self._Entries[0][j].winfo_width() for j in range(0, 4)]) + self._vsb.winfo_width()
        self._canvas_footer = Canvas(self._container, bg='lightgray', height = 30, width= widthFooter+400)
        self._canvas_footer.grid(row=self._beginRow+5, column=0, columnspan=11, sticky=N, padx=0, pady=0)
        self._frame_footer = Frame(self._canvas_footer, bg="lightgray")
        # self._frame_footer.grid(columnspan=5)
        
        self._canvas_footer.create_window((0, 0), window=self._frame_footer, anchor='nw')
        # self._labelFooter = Label(text=str_footer.format(name="admin", count=10, time=datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
        # self._labelFooter.grid(columnspan=5, sticky=W)
        # e = Label(self._frame_footer,text=" ").grid(row=0)
        self._label_str_topic_name = Button(self._frame_footer,text="Topic: ", bg="lightgray", font="Helvetica 11", anchor="center")
        self._label_topic_name = Button(self._frame_footer,text= "All", fg = "green", bg="lightgray", font="Helvetica 11", anchor="center",highlightthickness = 0, bd = 0)
        self._label_str_now = Button(self._frame_footer,text=chr(0x000023F1), bg="lightgray", font="Helvetica 11", anchor="center")
        self._label_now = Button(self._frame_footer,text= datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), fg = "green", bg="lightgray", font="Helvetica 11", anchor="center",highlightthickness = 0, bd = 0)
        self._label_str_account = Button(self._frame_footer,text="Account: ", bg="lightgray", font="Helvetica 11", anchor="center")
        self._label_topic_account = Button(self._frame_footer,text= "admin", fg = "red", bg="lightgray", font="Helvetica 11", anchor="center",highlightthickness = 0, bd = 0)
        self._label_str_total_count = Button(self._frame_footer,text="Total count: ", bg="lightgray", font="Helvetica 11", anchor="center")
        self._label_total_count = Button(self._frame_footer,text= "1", fg = "black", bg="lightgray", font="Helvetica 11", anchor="center",highlightthickness = 0, bd = 0)
        self._label_edit_mode = Button(self._frame_footer,text= "EDIT", fg = "Blue", bg="lightgray", font="Helvetica 11 bold", anchor="center",highlightthickness = 0, bd = 0)
        self._label_detail_mode = Button(self._frame_footer,text= "DETAIL", fg = "Blue", bg="lightgray", font="Helvetica 11 bold", anchor="center",highlightthickness = 0, bd = 0)
        self._btn_back = Button(self._frame_footer, text=chr(0x000023EA),width=3, height=1, font="Helvetica 14", anchor="center", bg="lightgray")
        self._btn_edit = Button(self._frame_footer, text=chr(0x0000270E),width=3, height=1, font="Helvetica 14", anchor="center", bg="lightgray", command=self.handle_click_edit)
        self._btn_refresh = Button(self._frame_footer, text=chr(0x0001F504),width=3, height=1, font="Helvetica 15", anchor=N, bg="lightgray", command=self.ReloadData)
        self._btn_disc = Button(self._frame_footer, text=chr(0x0001F4BF),width=3, height=1, font="Helvetica 15", anchor=N, bg="lightgray")
        self._btn_plus = Button(self._frame_footer, text=chr(0x00002795),width=3, height=1, font="Helvetica 15", anchor=N, bg="lightgray", command=self.__handler_plus)
        self._btn_eye = Button(self._frame_footer, text=chr(0x0001F441),width=3, height=1, font="Helvetica 15", anchor=N, bg="lightgray",command=self.handle_click_eye)
        # self._btn_edit = Button(self._frame_footer, text=chr(0x0001F589),width=5, height=1, font="Helvetica 10", anchor=N)
        # grid
        self._label_str_topic_name.grid(row=1,column=1)
        self._label_topic_name.grid(row=1,column=2) 
        self._label_str_now.grid(row=1,column=3) 
        self._label_now.grid(row=1,column=4) 
        self._label_str_account.grid(row=1,column=5) 
        self._label_topic_account.grid(row=1,column=6)
        self._label_str_total_count.grid(row=1,column=7) 
        self._label_total_count.grid(row=1,column=8) 
        self._btn_back.grid(row=1,column=9)
        self._btn_edit.grid(row=1,column=10)
        self._btn_refresh.grid(row=1,column=11)
        self._btn_disc.grid(row=1,column=12)
        self._btn_plus.grid(row=1,column=13)
        self._label_edit_mode.grid(row=1, column=15)
        self._label_detail_mode.grid(row=1, column=15)
        self._btn_eye.grid(row=1,column=14)
        self._label_edit_mode.grid_forget()
        self._label_detail_mode.grid_forget()
        self._frame_footer.update_idletasks()
        _thread.start_new_thread(self.LoadTime, ())

    def FrameWithScroll(self):  
        self._canvas = Canvas(self._container, bg="yellow")
        self._canvas.grid(row=self._beginRow+3, column=1, columnspan=5, sticky=NW)
        self._vsb = Scrollbar(self._container, orient="vertical", command=self._canvas.yview)
        self._vsb.grid(row=self._beginRow+3, column=1+ self._numbeCol, sticky='ns')
        self._vsb_h = Scrollbar(self._container, orient="horizontal", command=self._canvas.xview)
        self._vsb_h.grid(row=self._beginRow+4, column=1, sticky='ew', columnspan=4)
        self._canvas.configure(yscrollcommand=self._vsb.set, xscrollcommand=self._vsb_h.set)
        self._frame_tableData = Frame(self._canvas, bg="lightgray")
        self._frame_tableData.grid(columnspan=5)
        self._canvas.create_window((0, 0), window=self._frame_tableData, anchor='n')
        self.ReaderContentTable(20,4)
        self._canvas.config(scrollregion=self._canvas.bbox("all"))

    def __handler_plus(self):
        if self._isEdit:
            pass
        else:
            GUIEdit.GUIEditTopic(self.__dbIns).Render()

    def handle_click_entry(self, row):
        if self._isEdit and len(self._Entries[row][0].get())>0:
            print(row)
            for col in range(4):
                self._Entries[row][col].config(state=NORMAL)
            GUIEdit.GUIEditTopic(self.__dbIns, row+1).Render()
        if self._isDetail and len(self._Entries[row][0].get())>0:
            print(row)
            pass

    def handle_click_edit(self):
        if self._isEdit:
            self._isEdit = False
            self._label_edit_mode.grid_forget()
        elif self._isDetail is False:
            self._isEdit = True
            self._label_edit_mode.grid(row=1, column=15)

    def handle_click_eye(self):
        if self._isDetail:
            self._isDetail = False
            self._label_detail_mode.grid_forget()
        elif self._isEdit is False:
            self._isDetail = True
            self._label_detail_mode.grid(row=1, column=15)

    def ReaderContentTable(self, rows, columns):
        self._Entries = [[Entry() for j in range(columns)] for i in range(rows)]
        for i in range(0, rows):
            for j in range(0, columns):
                self._Entries[i][j] = Entry(self._frame_tableData, width=self._widthCols[j],fg='black',font=('Helvetica', 12, 'bold'),state="readonly")
                self._Entries[i][j].grid(row=i, column=j, sticky='news')
                self._Entries[i][j].bind("<1>",lambda e, row=i : self.handle_click_entry(row))
        
        self._frame_tableData.update_idletasks()

        canvas_width = sum([self._Entries[0][j].winfo_width() for j in range(0, 4)])
        canvas_height = self._Entries[0][0].winfo_height() * MAX_ROW_ONE_VIEW
        self._canvas.config(width=canvas_width,height=canvas_height)

    def LoadTime(self):
        while True:
            time.sleep(1)
            self._label_now.config(text=datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

    def ReloadData(self):
        print("reload data")
        keyData = ["No.", "Name", "CreateAt", "CreateBy"]
        rows = self.__dbIns.readTable("topic")
        for key in rows:
            data = rows[key]
            index = int(data['index']) -1
            for i in range(self._numbeCol):
                self._Entries[index][i].config(state=NORMAL)
                self._Entries[index][i].delete(0,END)
                if i == 0:
                    self._Entries[index][i].insert(END, data['index'])
                else:
                    self._Entries[index][i].insert(END, data['value'][keyData[i]])
                self._Entries[index][i].config(state="readonly")

    def Destroy(self):
        try:
            self._mainWindow.destroy()
        except Exception as e:
            print(r'[ERR] not init components !')
            print(r'[ERR] design\login.py line:49 ', e)

    def Render(self):
        try:
            self._mainWindow.mainloop()
        except Exception as e:
            print(r'[ERR] not init components !')
            print(r'[ERR] gui\login.py line:52 ', e)
