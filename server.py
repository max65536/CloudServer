import asyncio
from aiohttp import web
from handlers import store_file,download_file,api_register_user,api_login_user,login,register
from datalink import create_pool



async def init(loop):
    app = web.Application(loop=loop)

    app.router.add_route('POST', '/upload', store_file)
    app.router.add_route('POST', '/download', download_file)
    app.router.add_route('GET', '/login', login)
    app.router.add_route('GET', '/register', register)
    app.router.add_route('POST', '/api/register', api_register_user)
    app.router.add_route('POST', '/api/login', api_login_user)

    await create_pool(loop=loop, host='localhost', port=3306, user='root', password='Lqc1996812!', db='cloudserver')

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 8000)
    await site.start()
    print('Server started at http://127.0.0.1:8000...')
    return site

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()