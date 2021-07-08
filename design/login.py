from tkinter import *
from tkinter import messagebox as mb

class GUILogin:
    def __init__(self):
        self._mainWindow = Tk()
        self.login_entry = StringVar()
        self.password_entry = StringVar()
        beginRow = 0
        self._string_str_login = "Login"
        self._string_str_user = "Username"
        self._string_str_pass = "Password"
        self._string_str_hint_pass = "Saved password"
        self._string_error = "Incorrect password or username!"

        # components
        self._mainWindow.title("Login")
        self._mainWindow.geometry('300x180')
        self._mainWindow.resizable(width=False, height=False)
        self.chkValue = BooleanVar()
        self.chkValue.set(False)

        self._label_login = Label(self._mainWindow, text=self._string_str_login, font='Helvetica 15')
        self._label_user = Label(self._mainWindow, text=self._string_str_user, font='Helvetica 10 bold')
        self._label_password = Label(self._mainWindow, text=self._string_str_pass, font='Helvetica 10 bold')
        self._empty_user = Entry(self._mainWindow, width=30)
        self._empty_pass = Entry(self._mainWindow, width=30,show="*")
        self._checkbox_save_pass = Checkbutton(self._mainWindow, text=self._string_str_hint_pass, var=self.chkValue)

        self._btn_login = Button(self._mainWindow, text="Login", width=13, height=2, command=self.Destroy)
        self._label_error = Label(self._mainWindow, text=self._string_error, font='Helvetica 10 bold',  fg='red')

        # set location
        self._label_login.grid(row=beginRow+1, column=3, sticky=NW, columnspan=2, pady=4, padx=20)
        self._label_user.grid(row=beginRow+2, column=2, sticky=NW, pady=4, padx=20)
        self._label_password.grid(row=beginRow+3, column=2, sticky=NW, pady=4, padx=20)
        self._empty_user.grid(row=beginRow+2, column=3, sticky=NW, columnspan=2, pady=4)
        self._empty_pass.grid(row=beginRow+3, column=3, sticky=NW, columnspan=2, pady=4)
        self._checkbox_save_pass.grid(row=beginRow+4, column=2, columnspan=2, sticky=NW, pady=0, padx=30)
        self._btn_login.grid(row=beginRow+5, column=3, sticky=NW)
        self._label_error.grid_forget()

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


# GUILogin().Render()
    