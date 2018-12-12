import os
from config import config

def file_name():
    file_dir = os.getcwd() + '/ClientFiles/%s'%config['username']

    #print('Current directory is %s' % file_dir)
    for root, dirs, files in os.walk(file_dir):
        #print(root)
        #print(dirs)
        print(files)
    return files, file_dir
