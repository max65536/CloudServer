from file_name import file_name
from md5_check import md5_check
from md5_check import md5_file_content_check
from file_check import file_check
import threading
import requests,os
from config import config

filepath='./ClientFiles/userdata.txt'
datafile=open(filepath,'r')
username=datafile.read()
datafile.close()

def check_timer():
    rootpath='./ClientFiles/'+username
    if not os.path.exists(rootpath):
        os.mkdir(rootpath)
    f=open(rootpath+'/file_list.txt','wb')
    f.close()
    f=open(rootpath+'/md5_client01_file_content.txt','wb')
    f.close()
    f=open(rootpath+'/md5_client01.txt','wb')
    f.close()
    current_file_list, file_dir = file_name()
    current_file_list.remove('file_list.txt')
    current_file_list.remove('md5_client01_file_content.txt')
    current_file_list.remove('md5_client01.txt')
    current_md5 = md5_check(current_file_list, file_dir)
    md5_path = [file_dir + '/md5_client01.txt']
    with open(md5_path[0], 'w') as f:
        f.write(current_md5)
    # last_md5 = requests.get("http://127.0.0.1:8000/download/md5_client01.txt")
    last_md5 = download(username=username,filename='md5_client01.txt')
    last_md5_file_content_t = download(username=username,filename='md5_client01_file_content.txt')
    last_md5_file_content = last_md5_file_content_t.split('\n')
    current_md5_file_content = md5_file_content_check(current_file_list, file_dir)
    print('The MD5 in server is: %s' % last_md5)
    file_check(last_md5_file_content, current_md5_file_content, last_md5, current_md5, current_file_list, file_dir)
    global timer
    timer = threading.Timer(10, check_timer)
    timer.start()


def download(username,filename):
    params={
    'filename':filename,
    'name':username
    }
    re = requests.post("http://127.0.0.1:8000/download",data=params)
    return re.text
