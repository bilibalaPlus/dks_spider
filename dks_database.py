# encoding: utf-8

from peewee import *
import inspect
import datetime as dt
import sys

sys.path.append('.')
import dks_config as dc

host = dc.db['host']
user = dc.db['user']
passwd = dc.db['passwd']
database = dc.db['database']
charset = dc.db['charset']
mysql_db = MySQLDatabase(host = host,
                         user = user,
                         passwd = passwd,
                         database = database,
                         charset = charset)

class Task(Model):
    status = CharField()
    tasks = IntegerField(default = 0)
    finished = IntegerField(default = 0)
    unfinished = IntegerField(default = 0)
    failed = IntegerField(default = 0)
    created_at = DateTimeField(default = dt.datetime.now)
    class Meta:
        database = mysql_db

class Job(Model):
    task_id = IntegerField()
    source_id = IntegerField()
    status = CharField()
    message = CharField(default = '')
    created_at = DateTimeField(default = dt.datetime.now)
    updated_at = DateTimeField(default = dt.datetime.now)
    class Meta:
        database = mysql_db

class Source(Model): # DKS: 根据实际情况自行修改
    url = CharField()
    enabled = BooleanField(default = True)
    created_at = DateTimeField(default = dt.datetime.now)
    updated_at = DateTimeField(default = dt.datetime.now)
    class Meta:
        database = mysql_db

class Result(Model): # DKS: 根据实际情况自行修改
    content = CharField()
    source_id = IntegerField()
    created_at = DateTimeField(default = dt.datetime.now)
    updated_at = DateTimeField(default = dt.datetime.now)
    class Meta:
        database = mysql_db
        
class Worker(Model):
    name = CharField()
    address = CharField()
    updated_at = DateTimeField(default = dt.datetime.now)
    class Meta:
        database = mysql_db

if __name__ == '__main__': # 生成数据表
    try:
        tables = []
        for var in dir(sys.modules[__name__]):
            if var != 'Model':
                obj = eval(var)
                if inspect.isclass(obj) and issubclass(obj, Model):
                    tables.append(obj)
        mysql_db.connect()
        mysql_db.create_tables(tables, safe = True)
    except Exception as e:
        print(e)
    finally:
        mysql_db.close()
