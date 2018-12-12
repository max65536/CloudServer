

from orm import Model, StringField, BooleanField, FloatField, TextField
import time

class User(Model):
    """docstring for User"""
    def __init__(self, arg):
        super(User, self).__init__()
        self.arg = arg

    username=StringField(ddl='varchar(45)')
    password=StringField(ddl='varchar(45)')
    group=StringField(ddl='varchar(100)')
    device=StringField(ddl='varchar(100)')
    rootpath=StringField(ddl='varchar(100)')
    create_time=FloatField(default=time.time)


