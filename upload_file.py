import requests
from config import config

def upload_file(file_list):
    file_list_len = len(file_list)
    data = {"name" : config['username']}

    for num in range(file_list_len):
        filename = file_list[num]
        files = {
        "file": open("./ClientFiles/"+config['username']+'/'+filename, "rb")
        }
        r = requests.post("http://127.0.0.1:8000/upload", data, files=files)
        print(r.text)
