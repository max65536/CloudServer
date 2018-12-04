from upload_file import upload_file
import requests


def file_check(last_md5, current_md5, current_file_list, file_dir):
    if last_md5 == current_md5:
        print('both md5 are same\r\n\r\n')
    else:
        file_list_path = [file_dir + '/file_list.txt']
        with open(file_list_path[0], 'w') as f:
            for num in current_file_list:
                print(num, file=f)
        last_file_list_t = requests.get("http://127.0.0.1:8000/download/file_list.txt")
        upload_list = []
        if len(last_file_list_t.text) == 0:
            upload_list = current_file_list
            print('There is no such client before')
        else:
            current_num = 0
            last_num = 0
            last_file_list = last_file_list_t.text.split('\n')
            print('current %s' % current_file_list)
            print('last %s' % last_file_list)
            while current_num < len(current_file_list):
                if current_file_list[current_num] != last_file_list[last_num]:
                    upload_list.append(current_file_list[current_num])
                    current_num += 1
                else:
                    current_num += 1
                    last_num += 1
            upload_list.append('md5_client01.txt')
            upload_list.append('file_list.txt')
        upload_file(upload_list)
        print('upload files are %s\r\n\r\n' % upload_list)
