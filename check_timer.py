from file_name import file_name
from md5_check import md5_check
from md5_check import md5_file_content_check
from file_check import file_check
import threading
import requests,os
import tkinter as tk
import tkinter.messagebox
from config import config

filepath = './ClientFiles/userdata.txt'
datafile = open(filepath, 'r')
username = datafile.read()
datafile.close()


def flag_tk(value):
    global flagtk
    flagtk = value


def run_file_check(value=True):
    global runflag
    runflag = value


def check_timer():
    global last_md5_file_content, current_md5_file_content, last_md5, current_md5
    global current_file_list, last_file_list, file_dir
    global root1, ClientText, ServerText
    rootpath = './ClientFiles/'+username
    if not os.path.exists(rootpath):
        os.mkdir(rootpath)
    f = open(rootpath+'/file_list.txt', 'wb')
    f.close()
    f = open(rootpath+'/md5_client01_file_content.txt', 'wb')
    f.close()
    f = open(rootpath+'/md5_client01.txt', 'wb')
    f.close()
    current_file_list, file_dir = file_name()
    current_file_list.remove('file_list.txt')
    current_file_list.remove('md5_client01_file_content.txt')
    current_file_list.remove('md5_client01.txt')
    current_md5 = md5_check(current_file_list, file_dir)
    md5_path = [file_dir + '/md5_client01.txt']
    with open(md5_path[0], 'w') as f:
        f.write(current_md5)
    # last_md5 = requests.get("http://127.0.0.1:8000/download/md5_client01.txt")
    last_md5 = download(username=username,filename='md5_client01.txt')
    last_md5_file_content_t = download(username=username, filename='md5_client01_file_content.txt')
    last_md5_file_content = last_md5_file_content_t.split('\n')
    current_md5_file_content = md5_file_content_check(current_file_list, file_dir)
    print('The MD5 in server is: %s' % last_md5)
    print('The MD5 content in server is: %s' % last_md5_file_content)
    last_file_list_t = download(username=username, filename='file_list.txt')
    last_file_list = last_file_list_t.split('\n')
    print('The file list in server is: %s' % last_file_list)

    global flagtk
    if flagtk:
        root1 = tk.Tk()
        root1.geometry('600x400')
        root1.title('CloudServer-user: %s' % username)
        tk.Label(root1, text="ClientFile").place(x=135, y=20, width=80, height=10)
        tk.Label(root1, text="ServerFIle").place(x=385, y=20, width=80, height=10)
        ClientText = tk.Text(root1)
        ClientText.place(x=75, y=35, width=200, height=300)
        ServerText = tk.Text(root1)
        ServerText.place(x=325, y=35, width=200, height=300)
        vv = tk.IntVar()
        tk.Radiobutton(root1, text='Upload', variable=vv, value=1, command=run_file_check).place(x=200, y=345,width=100, height=30)
        tk.Radiobutton(root1, text='download', variable=vv, value=2).place(x=300, y=345, width=100, height=30)
        flag_tk(False)

    ClientText.delete("1.0", tk.END)
    for i in range(len(current_file_list)):
        ClientText.insert(tk.INSERT, current_file_list[i])
        ClientText.insert(tk.INSERT, "\n")

    ServerText.delete("1.0", tk.END)
    for i in range(len(last_file_list)):
        ServerText.insert(tk.INSERT, last_file_list[i])
        ServerText.insert(tk.INSERT, "\n")
    global runflag
    if runflag:
        file_check(last_md5_file_content, current_md5_file_content, last_md5, current_md5,
                   current_file_list, last_file_list, file_dir)
    global timer
    timer = threading.Timer(10, check_timer)
    timer.start()
    root1.mainloop()


def download(username, filename):
    params={
    'filename':filename,
    'name':username
    }
    re = requests.post("http://127.0.0.1:8000/download",data=params)
    return re.text

