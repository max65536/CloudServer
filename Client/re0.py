import requests
from config import config

# username=config['username']
# print(username)

# params={
#     'filename':'robot.png',
#     'name':'user5'
# }

# res=requests.get("http://127.0.0.1:8000/download",params=params)
# print(res)

# f=open('x.png','wb')
# f.write(res.content)

def download(username,filename):
    params={
    'filename':filename,
    'name':username
    }
    re = requests.post("http://127.0.0.1:8000/download",data=params)
    return re.text

def upload(username,filename):

    data = {"name" : username}
    f=open("./ClientFiles/"+username+'/'+filename, "rb")
    files = {
     "file": f
    }

    r = requests.post("http://127.0.0.1:8000/upload", data, files=files)

print(upload('ooo','Figure_1.png'))
