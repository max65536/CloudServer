import aiomysql,asyncio


async def create_pool(loop,**kw):
    #pool is used to reuse Conn Object
    global __pool
    __pool=await aiomysql.create_pool(
        host=kw.get('host','localhost'),
        #mysql default port is 3306,
        port=kw.get('port',3306),
        user=kw['user'],
        db=kw['db'],
        password=kw['password'],
        charset=kw.get('charset','utf8'),
        autocommit=kw.get('autocommit',True),
        maxsize=kw.get('maxsize',10),
        minsize=kw.get('minsize',1),
        loop=loop
        )

async def execute(sql,args,autocommit=True):
    '''args is a list or tuple'''
    with (await __pool) as conn:
        if not autocommit:
            conn.begin()
        try:
            cur=await conn.cursor()
            await cur.execute(sql.replace('?','%s'),args)
            affected=cur.rowcount
            await cur.close()
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
    return affected

async def select(sql,args,size=None):
    global __pool
    async with __pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            #DictCursor:A cursor which returns results as a dictionary. All methods and arguments same as Cursor
            await cur.execute(sql.replace('?','%s'),args or ())
            if size:
                rs= await cur.fetchmany(size)
            else:
                rs=await cur.fetchall()
        await cur.close()
        print('rows returned: %s' %len(rs))
        return rs

class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)

# StringField, BooleanField, FloatField, TextField
class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)

class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)

class IntegerField(Field):
    def __init__(self, name=None,primary_key=False,default=0):
        super().__init__(name, 'int', primary_key, default)

class FloatField(Field):
    def __init__(self, name=None,primary_key=False,default=0.0):
        super().__init__(name,'float',primary_key,default)

class TextField(Field):
    def __init__(self, name=None,primary_key=False,default=None):
        super().__init__(name,'text',False,default)


async def test(loop):
    await create_pool(loop=loop,host='localhost',port=3306,user='root',password='root',db='CloudServer')
    tableName='users'
    # sql= 'insert into `%s` (%s, `%s`) values (%s)' % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
    username='test1'
    password='abcdefg'
    sql = 'insert into %s (%s, %s) values (%s)' % (tableName, 'username','password',username+','+password)
    # print(sql)
    sql = 'insert into %s (%s, %s) values (%s,%s)'
    # await execute(sql,[tableName,'username','password',username,password])
    # u = User(username='Test1', passwd='1234567890', rootpath='/test1')
    # await u.save()
    # await User.findall()

async def test2(autocommit=True):
    # await test()
    with (await __pool) as conn:
        if not autocommit:
            conn.begin()
        try:
            cur=await conn.cursor()
            tableName='users'
            sql="insert into users (username, password) values ('test1','abcdefg')"
            sql = "insert into users (username, password) values (%s,%s)"
            args=['sdddaf','dsaf']
            await cur.execute(sql,args)
            affected=cur.rowcount
            await cur.close()
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
    print(affected)
    return affected

async def user_insert(username,password,autocommit=True):
    # await test()
    with (await __pool) as conn:
        if not autocommit:
            conn.begin()
        try:
            cur=await conn.cursor()
            tableName='users'
            # sql="insert into users (username, password) values ('test1','abcdefg')"
            sql = "insert into users (username, password, rootpath) values (%s,%s,%s)"
            rootpath='./Files/%s'%username
            args=[username,password,rootpath]
            await cur.execute(sql,args)
            affected=cur.rowcount
            await cur.close()
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
    print(affected)
    return affected

# async def find(pk):
#     'find object by Key'
#     rs=await select('select * from user %s where `%s`=?'%(cls.__select__,cls.__primary_key__),[pk],1)
#     if len(rs)==0:
#         return None
#     return cls(**rs[0])

def get_insert_sql(table,dict):
    sql='insert into %s'

# def dict2String(dict):
async def find(username,autocommit=True):
    # await test()
    with (await __pool) as conn:
        if not autocommit:
            conn.begin()
        try:
            cur=await conn.cursor()
            tableName='users'
            # sql="insert into users (username, password) values ('test1','abcdefg')"
            sql = "select * from users where username=%s"
            args=username
            # await select(sql,args)
            affected=await select(sql,args)
            await cur.close()
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
    print(affected)
    return affected


# loop=asyncio.get_event_loop()
# loop.run_until_complete(test_find())
