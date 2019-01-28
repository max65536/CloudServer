import os
import shutil

path='./ClientFiles/fff/1'

if os.path.exists(path):
    if os.path.isfile(path):
        os.remove(path)
    if os.path.isdir(path):
        shutil.rmtree(path)
else:
    print('no such file or directory:%s'%path)
