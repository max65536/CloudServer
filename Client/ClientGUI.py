import tkinter as tk
from tkinter.messagebox import showinfo,showerror
from Client import api_login

def usr_login():
    username=var_usr_name.get()
    password=var_usr_pwd.get()
    if api_login(username,password):
        showinfo(title='welcome',message='Hello'+username)
    else:
        showerror(message='username or password is wrong')

def usr_register():
    window_register=tk.Toplevel(window)
    window_register.geometry('350x200')
    window_register.title('register')

    new_name=tk.StringVar()
    tk.Label(window_register,text='username:').place(x=10,y=10)
    entry_new_name=tk.Entry(window_register,textvariable=new_name)
    entry_new_name.place(x=150,y=10)

    new_pwd=tk.StringVar()
    tk.Label(window_register,text='password:').place(x=10,y=50)
    entry_new_pwd=tk.Entry(window_register,textvariable=new_pwd,show='*')
    entry_new_pwd.place(x=150,y=50)

    new_pwd_confirm=tk.StringVar()
    tk.Label(window_register,text='Confirm password:').place(x=10,y=90)
    entry_new_pwd_confirm=tk.Entry(window_register,textvariable=new_pwd_confirm,show='*')
    entry_new_pwd_confirm.place(x=150,y=90)

    btn_confirm_register=tk.Button(window_register,text='register',command=register_to)

    btn_confirm_register.place(x=150,y=130)


def register_to():
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


