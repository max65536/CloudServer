from aiohttp import web
import re,os,time,hashlib
from datalink import user_insert,find


COOKIE_NAME='CloudServer'
_COOKIE_KEY='cloud'

def user2cookie(username,passwd,max_age):
    '''
    build cookie string by: id-expires-sha1
    "用户id" + "过期时间" + SHA1("用户id" + "用户口令" + "过期时间" + "SecretKey")
    '''
    expires=str(int(time.time()+max_age))
    s='%s-%s-%s-%s'%(username,passwd,expires,_COOKIE_KEY)
    L=[username,expires,hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

async def cookie2user(cookie_str):
    if cookie_str is None:
        return None
    try:
        L=cookie_str.split('-')
        if len(L)!=3:
            return None
        uid,expires,sha1=L
        # if int(expires)<time.time():
        #     return None
        user=await find(uid)
        if user is None:
            return None
        s='%s-%s-%s-%s'%(uid,user.passwd,expires,_COOKIE_KEY)
        if sha1!= hashlib.sha1(s.encode('utf-8')).hexdigest():
            print('invalid sha1')
        return user
    except Exception as e:
        print(e)
        raise None

def file_name(username):
    file_dir = os.getcwd() + '/Files/%s'%username

    #print('Current directory is %s' % file_dir)
    for root, dirs, files in os.walk(file_dir):
        #print(root)
        #print(dirs)
        print(files)
    return files, file_dir

def md5_check(file_list, file_dir):
    file_list_len = len(file_list)
    print('The number of files are is: %d' % file_list_len)
    md5_result = hashlib.md5(file_dir.encode('ascii'))
    for num in range(file_list_len):
        md5_result.update(file_list[num].encode('ascii'))
    print('MD5 is: %s' % (md5_result.hexdigest()))
    return md5_result.hexdigest()


def md5_file_content_check(file_list, file_dir):
    md5_file_content = []
    file_list_len = len(file_list)

    for num in range(file_list_len):        #read all files content and calculate their own md5
        with open(file_dir+'/'+file_list[num], 'rb') as f:
            content = f.read()
            md5_file_content.append(hashlib.md5(content).hexdigest())

    with open(file_dir + '/md5_client01_file_content.txt', 'w') as f:
        for num in md5_file_content:
            print(num, file=f)
    return md5_file_content

def md5_update(username):
    rootdir='./Files/%s'%username
    file_list=os.listdir(rootdir)
    md5_all=md5_check(file_list,rootdir)

async def login(request):
    login_file=open('./templates/login.html',encoding='utf-8')
    resp=web.Response(body=login_file.read().encode('utf-8'))
    resp.headers['content-type']='text/html'
    return resp

async def register(request):
    register_file=open('./templates/register.html',encoding='utf-8')
    resp=web.Response(body=register_file.read().encode('utf-8'))
    resp.headers['content-type']='text/html'
    return resp

async def store_file(request):
    # logging.info('upload image....................................')
    # logging.info(request.__data__)
    if request.method=='POST':
        data=await request.post()
        if data is None:
            return None
        file=data['file']
        if file is None:
            return None
        filename=file.filename
        username=data['name']
        file_content=file.file
        path='./Files/%s/%s'%(username,filename)
        new_file=open(path,'wb')
        for line in file_content:
            new_file.write(line)
        new_file.close()

        # current_file_list, file_dir = file_name(username)
        # current_file_list.remove('file_list.txt')
        # current_file_list.remove('md5_client01_file_content.txt')
        # current_file_list.remove('md5_client01.txt')
        # file_list_path = [file_dir + '/file_list.txt']
        # # file_dir='./Files/'+username
        # current_md5 = md5_check(current_file_list, file_dir)
        # md5_path = [file_dir + '/md5_client01.txt']
        # with open(md5_path[0], 'w') as f:
        #     f.write(current_md5)

        print(filename,' saved')
    return web.Response(text='file received')
        # 'path':path,

async def download_file(request):
    # filename=request.match_info['filename']
    # username=request.match_info['name']
    data=await request.post()
    print(data['name'])
    filename=data['filename']
    username=data['name']
    path='./Files/%s/%s'%(username,filename)
    return web.FileResponse(path)

# @post('/api/register')
async def api_register_user(request):
    # *后面的参数被视为命名关键字参数
    #todo: implement the find function
    # users= await User.findAll('email=?',[email])
    # if len(users)>0:
    #     print('register:failed','username','username is already registered')
    # sha1_passwd='%s:%s'%(uid,passwd)
    #sha1_passwd is a Hash String of 40 letters
    # print(request.method)
    # print(request.body)
    # print(request.POST)
    data=await request.json()
    print(data)
    username=data['name']
    passwd=data['passwd']
    print(username,':',passwd)
    rows=await user_insert(username=username,password=passwd)
    if rows>0:
        r=web.json_response('{text:successfully registered}')
        rootpath='./Files/%s'%username
        if not os.path.exists(rootpath):
            os.mkdir(rootpath)
        f=open(rootpath+'/file_list.txt','wb')
        f.close()
        f=open(rootpath+'/md5_client01_file_content.txt','wb')
        f.close()
        f=open(rootpath+'/md5_client01.txt','wb')
        f.close()
    else:
        r=web.Response(text='registration failed')
        r.set_cookie(COOKIE_NAME,user2cookie(username,passwd,86400),max_age=86400,httponly=True)
    return r

# @post('/login')
async def api_login_user(request):
    data=await request.json()
    print(data)
    # for a in data:
    #     print(a)
    username=data['name']
    passwd=data['passwd']
    print(username,':',passwd)
    rows=await find(username=username)
    if len(rows)>0:
        user=rows[0]
        print('user=',user)
        print('user["passwd"]=',user['password'])
        if passwd==user['password']:
            data = {'text': 'login successfully',
                    'path':user['rootpath']
                    }
            r=web.json_response(data)
            r.set_cookie(COOKIE_NAME,user2cookie(username,passwd,86400),max_age=86400,httponly=True)
            return r
            # message+='\n your directory:'+user['rootpath']
        else:
            message='login failed'
    else:
        message='login failed'
    r=web.Response(text=message)
    r.set_cookie(COOKIE_NAME,user2cookie(username,passwd,86400),max_age=86400,httponly=True)
    # print('-------------------------------')
    # print(COOKIE_NAME,':',user2cookie(user,86400))
    return r

