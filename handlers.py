from aiohttp import web


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
        file_content=file.file
        path='./Files/%s'%filename
        new_file=open(path,'wb')
        for line in file_content:
            new_file.write(line)
        new_file.close()
        print(filename,' saved')
    return web.Response(text='file received')
        # 'path':path,

async def download_file(request):
    filename=request.match_info['filename']
    path='./Files/%s'%filename
    return web.FileResponse(path)

