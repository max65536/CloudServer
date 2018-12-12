import requests
from config import config

username=config['username']
print(username)

params={
    'filename':'robot.png',
    'name':'user5'
}

res=requests.get("http://127.0.0.1:8000/download",params=params)
print(res)

f=open('x.png','wb')
f.write(res.content)


# headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
#                'Connection':'Keep-Alive',
#                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}

# keyword= "abc"

# res2=requests.get("https://www.google.de/search",params=keyword)
# print(res2)
# print(res2.content)

