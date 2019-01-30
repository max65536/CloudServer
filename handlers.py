from aiohttp import web
import re,os,time,hashlib,json
from datalink import user_insert,find
import shutil
import logging

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
        if int(expires)<time.time():
            return None
        rows=await find(uid)
        if rows is None:
            return None
        user=rows[0]
        # logging.info('user=',user)
        # print(cookie_str)
        s='%s-%s-%s-%s'%(uid,user["password"],expires,_COOKIE_KEY)
        if sha1!= hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
        return user
    except Exception as e:
        logging.info(e)
        raise None

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

# async def store_file(request):
#     # logging.info('upload image....................................')
#     # logging.info(request.__data__)
#     if request.method=='POST':
#         data=await request.post()
#         if data is None:
#             return None
#         file=data['file']
#         if file is None:
#             return None
#         # filename=file.filename
#         filename=data['filename']
#         username=data['name']
#         file_content=file.file
#         path='./Files/%s/%s'%(username,filename)

#         pa_dir=os.path.dirname(path)
#         if not os.path.exists(pa_dir):
#             os.makedirs(pa_dir)

#         with open(path,'wb') as f:
#             for line in file_content:
#                 f.write(line)

#         print(filename,' saved at ',path)
#     return web.Response(text='file received')

async def store_file(request):
    # logging.info('upload image....................................')
    # logging.info(request.__data__)
    if request.method=='POST':
        data=await request.post()
        if data is None:
            return None

        username=data['name']
        i=0
        while True:
            field='field%s'%i
            i+=1
            if field not in data:
                break
            file=data[field]
            filename=file.filename
            filecontent=file.file
            path='./Files/%s/%s'%(username,filename)
            pa_dir=os.path.dirname(path)
            if not os.path.exists(pa_dir):
                os.makedirs(pa_dir)

            with open(path,'wb') as f:
                for line in filecontent:
                    f.write(line)
            logging.info(filename+' saved at '+path)

        filelist=data['filelist']
        path='./Files/%s/%s'%(username,'md5_client01_file_content.txt')
        with open(path,'w') as f:
            f.write(filelist)

    return web.Response(text='file received')

async def delete_file(request):
    data=await request.post()
    if request.__user__ is None:
        return web.Response(text='please login first')
    username=request.__user__['username']
    filename=data['filename']
    filelist=data['filelist']
    path='./Files/%s/%s'%(username,'md5_client01_file_content.txt')
    with open(path,'w') as f:
        f.write(filelist)

    path='./Files/%s/%s'%(username,filename)
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
            logging.info('user %s delete file %s'%(username,path))
        if os.path.isdir(path):
            shutil.rmtree(path)
            logging.info('user %s delete directory %s'%(username,path))
        return web.Response(text='%s deleted'%filename)
    else:
        logging.info('no such file or directory:%s'%path)
        return web.Response(text='no such file or directory:%s'%path)


async def upload_json():
    if request.__user__ is None:
        return web.Response(text='user not found')
    username=request.__user__['username']

async def download_json(request):
    await request.post()
    if request.__user__ is None:
        return web.Response(text='user not found')
    username=request.__user__['username']

    # username='fff'

    path='./Files/%s/%s'%(username,'md5_client01_file_content.txt')
    with open(path) as f:
        content=f.read()

    resp=web.Response(body=content)
    resp.content_type='application/json;charset=utf-8'
    return resp



async def download_file(request):
    # filename=request.match_info['filename']
    # username=request.match_info['name']
    # print('COOKIE=:')
    # print(request.__user__)
    data=await request.post()
    if request.__user__ is None:
        return web.Response(text='login timeout, please login again')
    # print(data['name'])
    filename=data['filename']
    username=request.__user__['username']

    logging.info('user:%s download file %s'%(username,filename))

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
    # print(username,':',passwd)
    rows=await user_insert(username=username,password=passwd)
    if rows>0:
        # r=web.json_response('{text:successfully registered}')
        r=web.Response(text='successfully registered')
        logging.info('%s registered'%username)
        rootpath='./Files/%s'%username
        if not os.path.exists(rootpath):
            os.mkdir(rootpath)
        # f=open(rootpath+'/file_list.txt','w')
        # f.close()
        f=open(rootpath+'/md5_client01_file_content.txt','w')
        f.write('{}')
        f.close()
        # f=open(rootpath+'/md5_client01.txt','w')
        # f.close()
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
    # print(username,':',passwd)
    logging.info('%s login'% username)
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

async def test(request):
    print(request.__user__)

