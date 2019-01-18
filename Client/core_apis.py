import os
from config import config
import requests
import hashlib
import json

#file_name.py

def file_name():
    rootpath = './ClientFiles/userdata.txt'
    datafile = open(rootpath,'r')
    username = datafile.read()
    datafile.close()

    file_dir = os.getcwd() + '/ClientFiles/%s'%username

    #print('Current directory is %s' % file_dir)
    # for root, dirs, files in os.walk(file_dir):
    #     #print(root)
    #     #print(dirs)
    #     print(files)
    files=os.listdir(file_dir)
    return files, file_dir

#file_check.py

def file_content_check(last_md5_file_content,last_file_list, current_md5_file_content, current_file_list):
    update_list = []
    #print('length is %d' % len(current_md5_file_content))
    # num = 0
    # while(num < len(current_md5_file_content)):
    #     if current_md5_file_content[num] != last_md5_file_content[num]:
    #         update_list.append(current_file_list[num])
    #     num = num + 1
    if last_md5_file_content is not None:
        for key,value in last_md5_file_content.items():
            if (key not in current_md5_file_content) or current_md5_file_content[key]!=value:
                update_list.append(key)
    return update_list

def preprocess(L):
    print('L=',L)
    i=0
    # lenL=len(L)
    while i<len(L):
        if L[i]=='':
            L.pop(i)
        else:
            L[i]=L[i].strip('\r')
            i+=1


def file_check(last_md5_file_content,last_md5,last_file_list,current_md5_file_content,current_md5,current_file_list,file_dir):

    #preprocess
    # preprocess(last_md5_file_content)
    # preprocess(last_md5)
    preprocess(last_file_list)
    # preprocess(current_md5_file_content)
    # preprocess(current_md5)
    preprocess(current_file_list)

    # last_md5_file_content.pop()
    print('last list is %s' % last_md5_file_content)
    print('current list is %s' % current_md5_file_content)
    update_list = []

    if last_md5 == current_md5:
        update_list = file_content_check(last_md5_file_content, last_file_list,current_md5_file_content, current_file_list)
        print('update list is %s' % update_list) #[2]
        print('update list is %d' % len(update_list)) #0
        print('both name md5 are same')
    else:
        # if len(last_file_list) == 0:
        #     update_list = current_file_list
        #     print('There is no such client before')
        # else:
        print('current file list %s' % current_file_list)
        print('last file list%s' % last_file_list)
        ret_list = list(set(current_file_list)^set(last_file_list))
        update_list.extend(ret_list)

        content_update_list = file_content_check(last_md5_file_content,last_file_list, current_md5_file_content, current_file_list)
        print('content update is %s' % content_update_list)
        update_list.extend(content_update_list)

        print('update files are %s\r\n\r\n' % update_list)
    return update_list

#md5_check.py

def md5_check(file_list, file_dir):
    file_list_len = len(file_list)
    print('The number of files are is: %d' % file_list_len)
    md5_result = hashlib.md5(file_dir.encode('ascii'))
    for num in range(file_list_len):
        md5_result.update(file_list[num].encode('ascii'))
    print('MD5 is: %s' % (md5_result.hexdigest()))
    return md5_result.hexdigest()


def md5_file_content_check(file_list, file_dir):
    md5_file_content = {}

    for filename in file_list:        #read all files content and calculate their own md5
        with open(file_dir+'/'+filename, 'rb') as f:
            content = f.read()
            md5_file_content[filename]=hashlib.md5(content).hexdigest()

    with open(file_dir + '/md5_client01_file_content.txt', 'w') as f:
        jsObj=json.dumps(md5_file_content)
        f.write(jsObj)
    return md5_file_content

#upload_file.py

def upload_file(file_list):
    file_list.append('md5_client01.txt')
    file_list.append('file_list.txt')
    file_list.append('md5_client01_file_content.txt')
    file_list_len = len(file_list)
    rootpath = './ClientFiles/userdata.txt'
    datafile = open(rootpath,'r')
    username = datafile.read()
    datafile.close()

    data = {"name" : username}

    for num in range(file_list_len):
        filename = file_list[num]
        f=open("./ClientFiles/"+username+'/'+filename, "rb")
        files = {
         "file": f
        }
        # f.close()
        r = requests.post("http://127.0.0.1:8000/upload", data, files=files)
        print(r.text)

#download_file

def download_file(file_list):
    file_list.append('md5_client01.txt')
    file_list.append('file_list.txt')
    file_list.append('md5_client01_file_content.txt')
    file_list_len = len(file_list)
    rootpath = './ClientFiles/userdata.txt'
    datafile = open(rootpath,'r')
    username = datafile.read()
    datafile.close()

    data = {"name" : username,
            "filename":''
            }

    for num in range(file_list_len):
        filename = file_list[num]
        data['filename']=filename
        path='./ClientFiles/%s/%s'%(username,filename)
        # files = {
        #  "file": open("./ClientFiles/"+username+'/'+filename, "rb")
        # }
        r = requests.post("http://127.0.0.1:8000/download", data=data)
        # print(r.text)
        with open(path, "wb") as file:
            file.write(r.content)

