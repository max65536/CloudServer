import requests
import sys
import json
import os
from check_timer import check_timer
import threading,time
from core_apis2 import api_login,api_register,start_sync,delete_file

CMD_UPLOAD=0
CMD_DOWNLOAD=1
HOST='http://95.169.20.170'

def register():
    while True:
        username = input("username:")
        print(username)
        password1=input("password:")
        password2=input("repeat  :")
        print(password1,password2)
        if password2==password1:
            api_register(username,password1)
            break
        else:
            print("password not the same")

# def api_login(username,password):

#     resp=post_data(username,password,HOST+"/api/login")
#     if resp.text=='login failed':
#         return False

#     print("login as ",username)
#     print(resp.cookies[COOKIE_NAME])
#     cookie_str=(resp.cookies[COOKIE_NAME])
#     username = cookie_str.split('-')[0]
#     global USERNAME
#     USERNAME=username

#     dirs='./ClientFiles/%s/'%USERNAME
#     if not os.path.exists(dirs):
#         os.makedirs(dirs)

#     rootpath='./ClientFiles/userdata.txt'
#     f=open(rootpath,'w+')
#     f.write(username)
#     f.close()

#     download_configs(USERNAME)

#     check_timer(USERNAME,1,CMD_DOWNLOAD)
#     return True

def login():
    while True:
        username = input("username:")
        password=input("password:")
        re=api_login(username,password)
        if re:
            break
    print("login as ",username)


def check_forever(delay,command):
    while True:
        start_sync(delay,command)

def sync(delay,command):
    t=threading.Thread(target=check_forever,args=(delay,command))
    t.start()
    return t

def download(username,filename):
    params={
    'filename':filename,
    'name':username
    }
    re = requests.post(HOST+"/download",cookies=COOKIE,data=params)
    path='./ClientFiles/%s/%s'%(username,filename)
    print(path)
    pa_dir=os.path.dirname(path)
    print('pa_dir=',pa_dir)
    if not os.path.exists(pa_dir):
        os.makedirs(pa_dir)

    with open(path,'wb') as f:
        f.write(re.content)

    return re.text

def upload(username,filename):
    data = {"name" : username,
            "filename":filename
    }
    files = {
     "file": open("./ClientFiles/"+username+'/'+filename, "rb")
    }
    r = requests.post(HOST+"/upload", data, files=files)
    return 0

def writeCookie():
    filepath='ClientFiles/cookies.txt'
    with open('cookies.txt','w') as f:
        f.write(COOKIE)

def getCookie():
    pass

def entry():
    while True:
        command = input("command:")
        if command=='stop':
            break
        if command=='register':
            register()
            login()
        if command=='login':
            login()
        command = input("push or pull or delete:")
        if command=='push':
            sync(5,CMD_UPLOAD)
        if command=='pull':
            sync(5,CMD_DOWNLOAD)
        if command=='delete':
            filename = input("filename:")
            delete_file(filename)


if __name__ =='__main__':
    # entry()
    # sync('fff',5,CMD_UPLOAD)

    # login()
    # re=download('fff','md5_client01.txt')
    # print(COOKIE)
    # print('re=',re)
    # download_configs('fff')
    # upload('fff','1/scriptaculous.js')
    entry()

