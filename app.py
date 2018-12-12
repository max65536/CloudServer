import asyncio
from aiohttp import web
from handlers import store_file,download_file,api_register_user,api_login_user
from datalink import create_pool


# async def auth_factory(app,handler):
#     '''
#     to save the login status of user
#     '''
#     async def auth(request):
#         # print('check user:%s %s'%(request.method,request.path))
#         request.__user__=None
#         # cookie_str=request.cookies.get(COOKIE_NAME)
#         # if cookie_str:
#         #     user=await cookie2user(cookie_str)
#         #     if user:
#         #         request.__user__=user
#         return (await handler(request))
#     return auth

async def index(request):
    name=request.match_info['name']
    text='Hello,'+name

    return web.Response(text=text)

async def init(loop):
    app=web.Application(loop=loop)
    app.router.add_route('GET','/',index)
    app.router.add_route('GET','/{name}',index)
    app.router.add_route('POST','/upload',store_file)
    app.router.add_route('GET','/download',download_file)
    app.router.add_route('POST','/api/register',api_register_user)
    app.router.add_route('POST','/login',api_login_user)
    # app.router.add_route('GET','')
    await create_pool(loop=loop,host='localhost',port=3306,user='root',password='root',db='CloudServer')
    # srv=await loop.create_server(app.make_handler(),'127.0.0.1',8000)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    print('Server started at http://127.0.0.1:8000...')
    return srv

loop=asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
