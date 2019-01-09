import asyncio
import os,requests

from aiohttp import web

# username='test'
# rootpath='./Files/%s'%username
# os.mkdir(rootpath)

def download(username,filename):
    params={
    'filename':filename,
    'name':username
    }
    re = requests.post("http://127.0.0.1:8000/download",data=params)
    return re.text

download('ooo','Figure_1.png')
