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
    alldir,allfile=getallfiles(path)
    # for file in allfile:
    #     print(file)
    # print('alldir=',alldir)
    # print('allfile=',allfile)
    print('dir=',os.path.dirname('.\\ClientFiles\\userdata.txt'))
    file_dir=r'C:\Users\lz\Desktop\unibewerbungen\studium\gitshare\Groupwork\CloudServer\Client/ClientFiles/fff'
    file='C:\\Users\\lz\\Desktop\\unibewerbungen\\studium\\gitshare\\Groupwork\\CloudServer\\Client/ClientFiles/fff\\Pruefung.txt'
    print(os.path.relpath(file,file_dir))


