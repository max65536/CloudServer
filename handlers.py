from aiohttp import web
import re,os
from datalink import user_insert,find


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
        print(filename,' saved')
    return web.Response(text='file received')
        # 'path':path,

async def download_file(request):
    filename=request.match_info['filename']
    username=request.match_info['name']
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
            return web.json_response(data)
            # message+='\n your directory:'+user['rootpath']
        else:
            message='login failed'
    else:
        message='login failed'
    return web.Response(text=message)
