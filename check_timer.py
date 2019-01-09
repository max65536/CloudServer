from file_name import file_name
from md5_check import md5_check
from md5_check import md5_file_content_check
from file_check import file_check
from upload_file import upload_file
import threading
import requests
import time

filepath='./ClientFiles/userdata.txt'
datafile=open(filepath,'r')
username=datafile.read()
datafile.close()

def check_timer(delay):
    current_file_list, file_dir = file_name()
    current_file_list.remove('file_list.txt')
    current_file_list.remove('md5_client01_file_content.txt')
    current_file_list.remove('md5_client01.txt')
    current_md5 = md5_check(current_file_list, file_dir)
    md5_path = [file_dir + '/md5_client01.txt']
    with open(md5_path[0], 'w') as f:
        f.write(current_md5)
    last_md5 = download(username,'md5_client01.txt')
    last_md5 = last_md5
    last_md5_file_content_t = download(username,'md5_client01_file_content.txt')
    last_md5_file_content = last_md5_file_content_t.split('\n')
    last_file_list = download(username,'file_list.txt')
    last_file_list = last_file_list.split('\n')
    current_md5_file_content = md5_file_content_check(current_file_list, file_dir)
    print('The MD5 in server is: %s' % last_md5)
    upload_list = file_check(last_md5_file_content, current_md5_file_content, last_md5, current_md5,
                           current_file_list, last_file_list, file_dir)
    upload_file(upload_list)
    time.sleep(delay)
    print('checking......')

def download(username,filename):
    params={
    'filename':filename,
    'name':username
    }
    re = requests.post("http://127.0.0.1:8000/download",data=params)
    return re.text