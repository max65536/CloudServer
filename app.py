import asyncio
from aiohttp import web
from handlers import store_file,download_file,api_register_user,api_login_user,login,register,cookie2user,COOKIE_NAME,test,download_json,delete_file
from datalink import create_pool

import logging; logging.basicConfig(level=logging.INFO)


async def auth_factory(app,handler):
    '''
    to save the login status of user
    '''
    async def auth(request):
        # logging.info('check user:%s %s'%(request.method,request.path))
        request.__user__=None
        cookie_str=request.cookies.get(COOKIE_NAME)
        if cookie_str:
            user=await cookie2user(cookie_str)
            if user:
                request.__user__=user
                if request.path!=r'/download_json':
                    logging.info('user %s :%s %s'%(request.__user__['username'],request.method,request.path))
        return (await handler(request))
    return auth

async def index(request):
    # name=request.match_info['name']
    text='Hello,'+'world'

    return web.Response(text=text)

async def init(loop):
    app=web.Application(loop=loop,middlewares=[auth_factory])
    app.router.add_route('GET','/',index)
    app.router.add_route('GET','/test',test)
    # app.router.add_route('GET','/{name}',index)
    app.router.add_route('POST','/upload',store_file)
    app.router.add_route('POST','/download',download_file)
    app.router.add_route('POST','/delete',delete_file)

    app.router.add_route('POST','/download_json',download_json)

    app.router.add_route('GET','/login',login)
    app.router.add_route('GET','/register',register)
    app.router.add_route('POST','/api/register',api_register_user)
    app.router.add_route('POST','/api/login',api_login_user)
    # app.router.add_route('GET','')
    # app.router.add_static('/static/','./static')
    await create_pool(loop=loop,host='localhost',port=3306,user='root',password='root',db='cloudserver')
    # srv = await loop.create_server(app.make_handler(), host='127.0.0.1', port=8000)
    logging.info('Server started at http://127.0.0.1:9000...')
    return app

loop=asyncio.get_event_loop()
# loop.run_until_complete(init(loop))
# loop.run_forever()

app=loop.run_until_complete(init(loop))
web.run_app(app,host='127.0.0.1',port=9000,access_log=None)
