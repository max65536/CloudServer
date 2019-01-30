import tkinter as tk
from tkinter.messagebox import showinfo,showerror
from core_apis2 import api_login,api_register,start_sync,delete_file,get_delete_files
import os,time,threading

PATH='.'
CMD_UPLOAD=0
CMD_DOWNLOAD=1
ROOTPATH=''
FLAG=True

def listwindow(username):
    global ROOTPATH
    ROOTPATH='./ClientFiles/%s'%username
    windowlb = tk.Tk()
    windowlb.title('my windowlb')
    windowlb.geometry('400x600')

    var1 = tk.StringVar()    #创建变量
    var2 = tk.StringVar()    #创建变量
    l =tk.Label(windowlb,bg='white',width=30,textvariable=var1)
    l.pack()
    var1.set('welcome '+username)

    def print_selection():
        value = lb.get(lb.curselection())   #获取当前选中的文本
        var1.set(value)     #为label设置值

    def add_items(path):
        global PATH
        PATH=os.path.abspath(path)

        deletelist=get_delete_files()

        filelist=os.listdir(path)
        lb.insert('end', '..')
        lb.itemconfig(0,{'fg':'green'})
        for i in range(len(filelist)):
            lb.insert('end', filelist[i])  #从最后一个位置开始加入值
            if os.path.isdir(os.path.join(PATH,filelist[i])):
                lb.itemconfig(i+1,{'fg':'green'})
            file_path=os.path.join(PATH,filelist[i])
            rel_path=os.path.relpath(file_path,ROOTPATH)
            if rel_path in deletelist:
                lb.itemconfig(i+1,{'bg':'yellow'})

    def opendir():
        value = lb.get(lb.curselection())
        if value=='..':
            if os.path.relpath('./ClientFiles',os.path.dirname(PATH))=='.':
                return
            lb.delete(0,tk.END)
            add_items(os.path.dirname(os.path.join(PATH,value)))
        if os.path.isdir(os.path.join(PATH,value)):
            lb.delete(0,tk.END)
            # print('open=',os.path.join(PATH,value))
            add_items(os.path.join(PATH,value))

    def check_forever(delay,command):
        while True:
            start_sync(delay,command)

    def update_list(delay,command):
        while FLAG:
            print('updating...')
            time.sleep(delay)
            start_sync(delay,command)
            lb.delete(0,tk.END)
            add_items(PATH)

    def sync(delay,command):
        # t1=threading.Thread(target=check_forever,args=(delay,command))
        # t1.start()
        t2=threading.Thread(target=update_list,args=(delay,command))
        t2.start()
        return t2

    def upload_mode():
        # start_sync(5,CMD_UPLOAD)
        global FLAG
        FLAG=True
        sync(5,CMD_UPLOAD)
        var2.set('upload mode')
        # while FLAG:
        #     time.sleep(5)
        #     lb.delete(0,tk.END)
        #     add_items(PATH)

    def download_mode():
        global FLAG
        FLAG=True
        sync(5,CMD_DOWNLOAD)
        var2.set('download mode')

    def stop_mode():
        global FLAG
        FLAG=False
        print('stopped......')
        var2.set('stop mode')

    def delete_mode():
        value = lb.get(lb.curselection())
        file_path=os.path.join(PATH,value)
        rel_path=os.path.relpath(file_path,ROOTPATH)
        print('rel=',rel_path)
        delete_file(rel_path)
        lb.delete(0,tk.END)
        add_items(PATH)


    b1 = tk.Button(windowlb, text='open dir', width=30,
                  height=1, command=opendir)
    b1.pack()

    #创建Listbox

    lb = tk.Listbox(windowlb, width=50, height=20)  #将var2的值赋给Listbox

    add_items(PATH)
    #创建一个list并将值循环添加到Listbox控件中

    # lb.itemconfig(1,{'bg':'yellow'})

    # lb.insert(1, 'first')       #在第一个位置加入'first'字符
    # lb.insert(2, 'second')      #在第二个位置加入'second'字符
    # lb.delete(2)                #删除第二个位置的字符
    lb.pack()

    b_upload = tk.Button(windowlb, text='upload', width=30,
                  height=1, command=upload_mode)
    b_upload.pack()

    b_download = tk.Button(windowlb, text='download', width=30,
                  height=1, command=download_mode)
    b_download.pack()

    b_delete = tk.Button(windowlb, text='delete', width=30,
                  height=1, command=delete_mode)
    b_delete.pack()

    b_stop = tk.Button(windowlb, text='stop', width=30,
                  height=1, command=stop_mode)
    b_stop.pack()

    l2 =tk.Label(windowlb,bg='white',width=30,textvariable=var2)
    l2.pack()

    #显示主窗口
    windowlb.mainloop()



def usr_login():
    username=var_usr_name.get()
    password=var_usr_pwd.get()
    if api_login(username,password):
        showinfo(title='welcome',message='Welcome,'+username)
        window.destroy()
        # import test_list
        global PATH
        PATH='./ClientFiles/%s'%username
        listwindow(username)
    else:
        showerror(message='username or password is wrong')

def usr_register():

    window_register=tk.Toplevel(window)
    window_register.geometry('350x200')
    window_register.title('register')

    def register_to():
        username=new_name.get()
        password=new_pwd.get()
        password_con=new_pwd_confirm.get()
        if password==password_con:
            api_register(username,password)
            showinfo(title='success',message='%s successfully registered'%username)
            window_register.destroy()
        else:
            showerror(message='passwords not the same')


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


#####################LISTBOX#####################

