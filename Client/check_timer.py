from core_apis import file_name,md5_check,md5_file_content_check,file_check,upload_file,download_file
import threading
import requests
import time,json


filepath='./ClientFiles/userdata.txt'
datafile=open(filepath,'r')
username=datafile.read()
datafile.close()

CMD_UPLOAD=0
CMD_DOWNLOAD=1

def check_timer(delay,command):
    current_file_list, file_dir = file_name()
    current_file_list.remove('file_list.txt')
    current_file_list.remove('md5_client01_file_content.txt')
    current_file_list.remove('md5_client01.txt')
    file_list_path = [file_dir + '/file_list.txt']

    with open(file_list_path[0], 'w') as f:
        for num in current_file_list:
            print(num, file=f)

    current_md5 = md5_check(current_file_list, file_dir)
    md5_path = [file_dir + '/md5_client01.txt']

    with open(md5_path[0], 'w') as f:
        f.write(current_md5)

    last_md5 = download(username,'md5_client01.txt')
    last_md5 = last_md5
    last_md5_file_content_t = download(username,'md5_client01_file_content.txt')
    print('last_md5_file_content_t=',last_md5_file_content_t)
    if last_md5_file_content_t=='':
        last_md5_file_content=None
    else:
        last_md5_file_content = json.loads(last_md5_file_content_t)
    #move pop here
    # last_md5_file_content.pop()

    last_file_list = download(username,'file_list.txt')
    last_file_list = last_file_list.split('\n')
    current_md5_file_content = md5_file_content_check(current_file_list, file_dir)
    print('The MD5 in server is: %s' % last_md5)

    if command==CMD_UPLOAD:
        upload_list = file_check(last_md5_file_content,last_md5,last_file_list,current_md5_file_content,current_md5,current_file_list,file_dir)
        upload_file(upload_list)
        time.sleep(delay)
        print('sync Client to Server......')

    if command==CMD_DOWNLOAD:
        download_list = file_check(current_md5_file_content,current_md5,current_file_list,last_md5_file_content,last_md5,last_file_list,file_dir)
        download_file(download_list)
        time.sleep(delay)
        print('sync Server to Client......')

def download(username,filename):
    params={
    'filename':filename,
    'name':username
    }
    re = requests.post("http://127.0.0.1:8000/download",data=params)
    return re.text
