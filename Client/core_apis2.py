import os,json,hashlib
import requests,time,shutil

CMD_UPLOAD=0
CMD_DOWNLOAD=1
COOKIE_NAME='CloudServer'
USERNAME='fff'
# COOKIE={"CloudServer": "fff-1548694821-52bbae7526649fc6aeb7d80bdd4771717b37484e"}
COOKIE=''
HOST='http://95.169.20.170'
# HOST='http://127.0.0.1:9000'

def get_filelist(username):
    file_dir = os.getcwd() + '/ClientFiles/%s'%username
    allfile=[]
    alldir=[]
    for dirpath,dirnames,filenames in os.walk(file_dir):
        for dir in dirnames:
            alldir.append(os.path.join(dirpath,dir))
        for filename in filenames:
            filepath=os.path.join(dirpath, filename)
            allfile.append(os.path.relpath(filepath,file_dir))
    return alldir,allfile,file_dir

def get_localdict(username):
    alldir,file_list,file_dir=get_filelist(username)
    md5_file_content = {}
    for filename in file_list:
    #read all files content and calculate their own md5
        with open(file_dir+'/'+filename, 'rb') as f:
            content = f.read()
            md5_file_content[filename]=hashlib.md5(content).hexdigest()
    return md5_file_content

def get_serverlist():
    pass

def get_updatelist(dictA,dictB):
    '''
        assume A>B.
        compare dictA with dictB and return dictA-dictB,
        if A has x and B does not, then add x into updatelist.
    '''
    update_list = []
    if dictA:
        # print('dictA=',dictA)
        for key,value in dictA.items():
            if (key not in dictB) or dictB[key]!=value:
                update_list.append(key)
    return update_list

def file_compare():
    pass

def getjson():
    re = requests.post(url=HOST+"/download_json",cookies=COOKIE)
    # print(re)
    serverlist=json.loads(re.text)
    print('COOKIE=',COOKIE)
    # print('serverdict=',serverlist)
    return serverlist

# def upload_all():
#     serverdict=getjson()
#     localdict=get_localdict(USERNAME)
#     file_list=get_updatelist(localdict,serverdict)

#     username=USERNAME
#     data = {"name" : username}

#     for filename in file_list:
#         path='./ClientFiles/%s/%s'%(username,filename)
#         f=open(path, "rb")
#         files = {
#          "file": f
#         }
#         data['filename']=filename
#         r = requests.post(HOST+"/upload", data=data,cookies=COOKIE, files=files)
def get_delete_files():
    serverdict=getjson()
    localdict=get_localdict(USERNAME)
    update_list=get_updatelist(localdict,serverdict)
    return update_list

def upload_all():
    serverdict=getjson()
    localdict=get_localdict(USERNAME)
    update_list=get_updatelist(localdict,serverdict)

    username=USERNAME
    data = {"name" : username,
            "filelist":json.dumps(localdict)}
    # print('localdict=',localdict)
    # print('serverdict=',serverdict)
    # print('filelist=',json.loads(data['filelist']))
    # print('update_list=',update_list)
    files={}
    i=0
    for filename in update_list:
        path='./ClientFiles/%s/%s'%(username,filename)
        f=open(path, "rb")
        files['field%s'%i]=(filename,f)
        i+=1
        data['filename']=filename
    # print('files=',files)
    print('update_list=',update_list)
    if len(update_list)>0:
        r = requests.post(HOST+"/upload", data=data,cookies=COOKIE, files=files)

def download_all():
    serverdict=getjson()
    localdict=get_localdict(USERNAME)
    file_list=get_updatelist(serverdict,localdict)

    # print('serverdict=',serverdict)
    # print('localdict=',localdict)
    # print('filelist=',file_list)
    username=USERNAME

    data = {"name" : username,
            "filename":''
            }

    for filename in file_list:
        data['filename']=filename
        path='./ClientFiles/%s/%s'%(username,filename)
        r = requests.post(HOST+"/download", cookies=COOKIE,data=data)
        pa_dir=os.path.dirname(path)
        if not os.path.exists(pa_dir):
            os.makedirs(pa_dir)
        with open(path, "wb") as file:
            file.write(r.content)

def delete_file(filename):
    path='./ClientFiles/%s/%s'%(USERNAME,filename)
    olddict=get_localdict(USERNAME)
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        if os.path.isdir(path):
            shutil.rmtree(path)
        localdict=get_localdict(USERNAME)
        file_list=get_updatelist(olddict,localdict)
        data={
                'filelist':json.dumps(localdict),
                'filename':filename
                }
        r = requests.post(HOST+"/delete", cookies=COOKIE,data=data)
    else:
        print('no such file or directory:%s'%path)

def post_data(username,password,url):
    headers = {'Content-Type': 'application/json'}
    data={
            "name":username,
            "passwd":password
    }
    r = requests.post(url=url, headers=headers,data=json.dumps(data))
    print(r.text)
    return r

def api_register(username,password):
    resp=post_data(username,password,HOST+"/api/register")

    rootpath='./ClientFiles/'+username
    if not os.path.exists(rootpath):
        os.mkdirs(rootpath)

    print(resp.cookies[COOKIE_NAME])
    cookie_str=(resp.cookies[COOKIE_NAME])
    username = cookie_str.split('-')[0]
    global COOKIE
    COOKIE={COOKIE_NAME:cookie_str}
    global USERNAME
    USERNAME=username

def api_login(username,password):

    resp=post_data(username,password,HOST+"/api/login")
    if resp.text=='login failed':
        return False

    print("login as ",username)
    print(resp.cookies[COOKIE_NAME])
    cookie_str=(resp.cookies[COOKIE_NAME])
    username = cookie_str.split('-')[0]
    global COOKIE
    COOKIE={COOKIE_NAME:cookie_str}
    global USERNAME
    USERNAME=username

    dirs='./ClientFiles/%s/'%USERNAME
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    return True

def start_sync(delay,command):
    print('username=',USERNAME,'   COOKIE=',COOKIE)
    if command==CMD_UPLOAD:
        upload_all()
        # time.sleep(delay)
        print('sync Client to Server......')

    if command==CMD_DOWNLOAD:
        download_all()
        # time.sleep(delay)
        print('sync Server to Client......')


if __name__=='__main__':
    # filelist=get_localdict('fff')
    # print(filelist)
    # api_login('fff','fff')
    # api_register('xxx','xxx')
    # print(COOKIE)
    # global COOKIE
    # COOKIE="{'CloudServer': 'fff-1548694821-52bbae7526649fc6aeb7d80bdd4771717b37484e'}"
    global COOKIE
    COOKIE=json.loads(COOKIE)

    # download_all()
    # upload_all()
    delete_file('1')
    # download_all()


    # print(COOKIE)
    # print(json.loads(COOKIE))
    # print(getjson())
