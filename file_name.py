import os


def file_name():
    file_dir = os.getcwd() + '/shared_files'
    print('Current directory is %s' % file_dir)
    for root, dirs, files in os.walk(file_dir):
        #print(root)
        #print(dirs)
        print('Current files are %s' % files)
    return files, file_dir
