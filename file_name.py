import os
from config import config


def file_name():
    rootpath = './ClientFiles/userdata.txt'
    datafile = open(rootpath,'r')
    username = datafile.read()
    datafile.close()

    file_dir = os.getcwd() + '/ClientFiles/%s'%username

    #print('Current directory is %s' % file_dir)
    for root, dirs, files in os.walk(file_dir):
        #print(root)
        #print(dirs)
        print(files)
    return files, file_dir
