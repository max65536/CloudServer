import requests
import sys
import json
import os
# from client01 import time_start

COOKIE_NAME='CloudServer'
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
        if password2==password1:
            post_data(username,password1,"http://127.0.0.1:8000/api/register")
            rootpath='./ClientFiles/'+username
            if not os.path.exists(rootpath):
                os.mkdir(rootpath)
            f=open(rootpath+'/file_list.txt','wb')
            f.close()
            f=open(rootpath+'/md5_client01_file_content.txt','wb')
            f.close()
            f=open(rootpath+'/md5_client01.txt','wb')
            f.close()
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
    rootpath='./ClientFiles/userdata.txt'
    f=open(rootpath,'w+')
    f.write(username)
    f.close()

    sync()
    # datafile=open(rootpath,'r')
    # data=datafile.read()
    # print(data)

def sync():
    time_start()

# login()
def download(username,filename):
    params={
    'filename':filename,
    'name':username
    }
    re = requests.post("http://127.0.0.1:8000/download",data=params)
    with open("demo3.txt", "wb") as code:
         code.write(re.content)
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
        if command=='login':
            login()
if __name__ =='__main__':
    entry()
# download('ooo','file_list.txt')


