import tkinter as tk
from tkinter.messagebox import showinfo
from Client import api_login,check_timer

def usr_login():
    username=var_usr_name.get()
    password=var_usr_pwd.get()
    showinfo(message='Hello,'+username)

def usr_register():
    pass

window=tk.Tk()
window.title('Client')
window.geometry('400x300')
# canvas=tk.Canvas(window,height=200,width=500)

tk.Label(window,text='username:').place(x=50,y=150)
tk.Label(window,text='password:').place(x=50,y=190)

var_usr_name=tk.StringVar()
# var_usr_name.set('example@mail.com')
entry_usr_name=tk.Entry(window,textvariable=var_usr_name)
entry_usr_name.place(x=160,y=150)
var_usr_pwd=tk.StringVar()
entry_usr_pwd=tk.Entry(window,textvariable=var_usr_pwd,show='*')
entry_usr_pwd.place(x=160,y=190)

btn_login=tk.Button(window,text='Login',command=usr_login)
btn_login.place(x=170,y=230)
btn_register=tk.Button(window,text='register',command=usr_register)
btn_register.place(x=270,y=230)

window.mainloop()


