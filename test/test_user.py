import requests
import json

# filename='robot.png'
postData = {
    'name':'user2',
    'passwd':'123456'
}

s = json.dumps(postData)
def login(name='user2',passwd='123456'):
    postData = {
    'name':name,
    'passwd':passwd
    }
    r = requests.post("http://127.0.0.1:8000/login", data=postData)
    print(r.text)
    return
# r = requests.get('https://www.google.com')

def register(name='user2',passwd='123456'):
    postData = {
    'name':name,
    'passwd':passwd
    }
    r = requests.post("http://127.0.0.1:8000/api/register", data=postData)
    print(r.text)
    return

# login()
register(name='user6',passwd='laallll')
