import tkinter as tk
import os,time,threading
from core_apis2 import start_sync,delete_file

PATH='./ClientFiles/fff'
ROOTPATH='./ClientFiles/fff'
FLAG=True
CMD_UPLOAD=0
CMD_DOWNLOAD=1
# PATH=os.getcwd()

windowlb = tk.Tk()
windowlb.title('my windowlb')
windowlb.geometry('400x600')

var1 = tk.StringVar()    #创建变量
var2 = tk.StringVar()    #创建变量
l =tk.Label(windowlb,bg='white',width=30,textvariable=var1)
l.pack()

def print_selection():
    value = lb.get(lb.curselection())   #获取当前选中的文本
    var1.set(value)     #为label设置值

def add_items(path):
    global PATH
    PATH=os.path.abspath(path)
    filelist=os.listdir(path)
    lb.insert('end', '..')
    lb.itemconfig(0,{'fg':'green'})
    for i in range(len(filelist)):
        lb.insert('end', filelist[i])  #从最后一个位置开始加入值
        if os.path.isdir(os.path.join(PATH,filelist[i])):
            lb.itemconfig(i+1,{'fg':'green'})

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
