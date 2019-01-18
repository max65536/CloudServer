from check_timer import check_timer, flag_tk, run_file_check
import threading
import requests
import tkinter as tk
import tkinter.messagebox
import json
import os
import time


def login():
    global flagLogReg
    flagLogReg = 0
    global root
    tk.Label(root, text="username").place(x=30, y=50, width=100, height=30)
    tk.Label(root, text="password").place(x=30, y=80, width=100, height=30)
    tk.Label(root, text="        ").place(x=30, y=110, width=200, height=30)
    global LogStrUsername, LogStrPassword
    LogStrUsername = tk.StringVar()
    e1 = tk.Entry(root, textvariable=LogStrUsername)
    e1.place(x=130, y=50, width=100, height=30)
    LogStrPassword = tk.StringVar()
    e2 = tk.Entry(root, textvariable=LogStrPassword)
    e2.place(x=130, y=80, width=100, height=30)


def register():
    global flagLogReg
    flagLogReg = 1
    global root
    tk.Label(root, text="username").place(x=30, y=50, width=100, height=30)
    tk.Label(root, text="password").place(x=30, y=80, width=100, height=30)
    tk.Label(root, text="repeat").place(x=30, y=110, width=100, height=30)
    global RegStrUsername, RegStrPassword, RegStrRepeat
    RegStrUsername = tk.StringVar()
    e1 = tk.Entry(root, textvariable=RegStrUsername)
    e1.place(x=130, y=50, width=100, height=30)
    RegStrPassword = tk.StringVar()
    e2 = tk.Entry(root, textvariable=RegStrPassword)
    e2.place(x=130, y=80, width=100, height=30)
    RegStrRepeat = tk.StringVar()
    e3 = tk.Entry(root, textvariable=RegStrRepeat)
    e3.place(x=130, y=110, width=100, height=30)


def post_data(username,password,url):
    headers = {'Content-Type': 'application/json'}
    data={
            "name":username,
            "passwd":password
    }
    r = requests.post(url=url, headers=headers,data=json.dumps(data))
    print(r.text)
    return r


def register1():
    global RegStrUsername, RegStrPassword, RegStrRepeat
    while True:
        username = RegStrUsername.get()
        print(username)
        password1 = RegStrPassword.get()
        password2 = RegStrRepeat.get()
        print(password1, password2)
        if password2 == password1:
            tk.messagebox.showinfo("info", "register ok")
            post_data(username,password1, "http://127.0.0.1:8000/api/register")
            rootpath = './ClientFiles/'+username
            if not os.path.exists(rootpath):
                os.mkdir(rootpath)
            f = open(rootpath+'/file_list.txt', 'wb')
            f.close()
            f = open(rootpath+'/md5_client01_file_content.txt', 'wb')
            f.close()
            f = open(rootpath+'/md5_client01.txt', 'wb')
            f.close()
            break
        else:
            print("password not the same")


def login1():
    global LogStrUsername, LogStrPassword
    while True:
        username = LogStrUsername.get()
        password = LogStrPassword.get()
        resp = post_data(username, password, "http://127.0.0.1:8000/api/login")
        if resp.text != 'login failed':
            break

    print("login as ", username)
    print(resp.cookies['CloudServer'])
    rootpath = './ClientFiles/userdata.txt'
    f = open(rootpath, 'w+')
    f.write(username)
    f.close()

    # while True:
    check_timer()
    time.sleep(2)
    print('sleep-----------')



def entry():
    global flagLogReg
    global root
    root.destroy()
    if flagLogReg == 1:
        register1()
    if flagLogReg == 0:
        flag_tk(True)
        run_file_check(False)
        login1()


def root_func():
    global root
    return root


global root
root = tk.Tk()
root.geometry('300x300')
root.title('CloudServer')
global flagLogReg #Login=0,Register=1
flagLogReg = 0

v = tk.IntVar()
v.set(1)
login()
tk.Radiobutton(root, text='login', variable=v, value=1, command=login).place(x=70, y=150, width=60, height=30)
tk.Radiobutton(root, text='register', variable=v, value=2, command=register).place(x=130, y=150, width=100, height=30)
global Entry
Entry = tk.Button(root, text='Entry', command=entry).place(x=100, y=180, width=100, height=30)
root.mainloop()


