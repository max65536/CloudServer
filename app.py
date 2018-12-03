import asyncio
from aiohttp import web
from handlers import store_file,download_file


async def index(request):
    name='aaa'
    name=request.match_info['name']
    text='Hello'+name
    return web.Response(text=text)

async def init(loop):
    app=web.Application(loop=loop)
    app.router.add_route('GET','/',index)
    app.router.add_route('GET','/{name}',index)
    app.router.add_route('POST','/upload',store_file)
    app.router.add_route('GET','/download/{filename}',download_file)
    # srv=await loop.create_server(app.make_handler(),'127.0.0.1',8000)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    print('Server started at http://127.0.0.1:8000...')
    return srv

loop=asyncio.get_event_loop()


loop.run_until_complete(init(loop))
loop.run_forever()


