import requests
from config import config


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
        files = {
         "file": open("./ClientFiles/"+username+'/'+filename, "rb")
        }
        r = requests.post("http://127.0.0.1:8000/upload", data, files=files)
        print(r.text)


