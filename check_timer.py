from file_name import file_name
from md5_check import md5_check
from file_check import file_check
import threading
import requests

def check_timer():
    current_file_list, file_dir = file_name()
    current_md5 = md5_check(current_file_list, file_dir)
    md5_path = [file_dir + '/md5_client01.txt']
    with open(md5_path[0], 'w') as f:
        f.write(current_md5)
    last_md5 = requests.get("http://127.0.0.1:8000/download/md5_client01.txt")
    last_md5 = last_md5.text
    print('The MD5 in server is: %s' % last_md5)
    file_check(last_md5, current_md5, current_file_list, file_dir)
    global timer
    timer = threading.Timer(10, check_timer)
    timer.start()
