import os

def getallfiles(path):
    allfile=[]
    alldir=[]
    for dirpath,dirnames,filenames in os.walk(path):
        # print(filenames)
        for dir in dirnames:
            alldir.append(os.path.join(dirpath,dir))
        for name in filenames:
            allfile.append(os.path.join(dirpath, name))
    return alldir,allfile
if  __name__ == '__main__':
    path = "."
    # for dirpath,dirnames,filenames in os.walk(path):
    #     print('dirpath=',dirpath)
    #     print('dirnames=',dirnames)
    #     print('filenames=',filenames)
    # print(os.listdir(path))
    # print('dir=',os.path.dirname(os.path.abspath('check_timer.py')))
    # print(os.path.isdir('__pycache__'))
    # for file in allfile:
    #     print(file)
    # print('alldir=',alldir)
    # print('allfile=',allfile)
    # print('dir=',os.path.dirname('.\\ClientFiles\\userdata.txt'))
    # file_dir=r'C:\Users\lz\Desktop\unibewerbungen\studium\gitshare\Groupwork\CloudServer\Client/ClientFiles/fff'
    # file='C:\\Users\\lz\\Desktop\\unibewerbungen\\studium\\gitshare\\Groupwork\\CloudServer\\Client/ClientFiles/fff\\Pruefung.txt'
    # print(os.path.relpath(file,file_dir))

    # filelist=os.listdir('./ClientFiles/ggg')
    # print(filelist)
    # print(os.path.abspath('user10'))
    # print(os.path.isdir('./ClientFiles/ggg/user10'))
    # print(os.path.isfile(os.path.abspath('user10')))
    PATH='./ClientFiles/fff'
    pathnow=os.getcwd()
    par_path='./Client'
    rel_path=os.path.relpath(os.path.join(PATH,'user6\\md5_client01.txt'),PATH)
    print(os.getcwd())
    print(os.path.dirname(os.getcwd()))
    print('rel=',rel_path)
