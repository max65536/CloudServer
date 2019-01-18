import requests
import sys
import json
import os
from check_timer import check_timer
import threading,time

COOKIE_NAME='CloudServer'

CMD_UPLOAD=0
CMD_DOWNLOAD=1
# data = {"name" : "user5"}
# filename='robot.png'
# files = {
#   "file" : open("./ClientFiles/"+filename, "rb")
# }
# r = requests.post("http://127.0.0.1:8000/upload", data, files=files)

# r = requests.get('https://www.google.com')
# print(r.text)
def post_data(username,password,url):
    headers = {'Content-Type': 'application/json'}
    data={
            "name":username,
            "passwd":password
    }
    r = requests.post(url=url, headers=headers,data=json.dumps(data))
    print(r.text)
    return r

def register():
    while True:
        username = input("username:")
        print(username)
        password1=input("password:")
        password2=input("repeat  :")
        print(password1,password2)

        rootpath='./ClientFiles/userdata.txt'
        f=open(rootpath,'w+')
        f.write(username)
        f.close()

        if password2==password1:
            post_data(username,password1,"http://127.0.0.1:8000/api/register")
            rootpath='./ClientFiles/'+username
            if not os.path.exists(rootpath):
                os.mkdir(rootpath)

            f=open(rootpath+'/file_list.txt','wb')
            f.close()
            upload(username,'file_list.txt')
            f=open(rootpath+'/md5_client01_file_content.txt','wb')
            f.close()
            upload(username,'md5_client01_file_content.txt')
            f=open(rootpath+'/md5_client01.txt','wb')
            f.close()
            upload(username,'md5_client01.txt')


            break
        else:
            print("password not the same")

# register()
def login():
    while True:
        username = input("username:")
        password=input("password:")
        resp=post_data(username,password,"http://127.0.0.1:8000/api/login")
        if resp.text!='login failed':
            break

    print("login as ",username)
    print(resp.cookies[COOKIE_NAME])
    cookie_str=(resp.cookies[COOKIE_NAME])
    username = cookie_str.split('-')[0]
    rootpath='./ClientFiles/userdata.txt'
    f=open(rootpath,'w+')
    f.write(username)
    f.close()

    check_timer(1,CMD_DOWNLOAD)

    # datafile=open(rootpath,'r')
    # data=datafile.read()
    # print(data)

def check_forever(delay,command):
    while True:
        check_timer(delay,command)

def sync(delay,command):
    t=threading.Thread(target=check_forever,args=(delay,command))
    t.start()
    return t

# login()
def download(username,filename):
    params={
    'filename':filename,
    'name':username
    }
    re = requests.post("http://127.0.0.1:8000/download",data=params)
    print(re.text)
    with open("demo3.txt", "wb") as code:
         code.write(re.content)
    return 0

def upload(username,filename):
    data = {"name" : username}
    files = {
     "file": open("./ClientFiles/"+username+'/'+filename, "rb")
    }
    r = requests.post("http://127.0.0.1:8000/upload", data, files=files)
    return 0

def addCookie():
    pass

def getCookie():
    pass

def entry():
    while True:
        command = input("command:")
        if command=='register':
            register()
            login()
        if command=='login':
            login()
        command = input("push or pull:")
        if command=='push':
            sync(3,CMD_UPLOAD)
        if command=='pull':
            sync(3,CMD_DOWNLOAD)


if __name__ =='__main__':
    entry()
    # sync(3,CMD_DOWNLOAD)


    # download('ooo','file_list.txt')


