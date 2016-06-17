#! /usr/bin/ python3
# -*- coding: urf-8 -*-

__author__ = 'lichenjie'

import asyncio, logging

def log(sql, args=()):
  logging.info('SQL: %s' % sql)

async def create_pool(loop, **kw):
  logging.info('create database connection pool...')
  global __pool
  __pool = await aiomysql.create_pool(
    host=kw.get('host', 'localhost')
    port=kw.get('port', 3306)
    user=kw['user']
    password=kw['password']
    db=kw['db']
    charset=kw.get('charset', 'utf8')
    autocommit=kw.get('autocommit', True)
    maxsize=kw.get('maxsize', 10)
    minisize=kw.get('minisize', 1),
    loop=loop
  )

async def select(sql. args, size=None):
  log(sql, args)
  global __pool
  async with __pool.get() as conn:
   cur = yield from conn.curor(aiomysql.DictCursor)
   yield from cur.execute(sql.replace('?', '%s'), args or ())
   if size:
     rs = yield from cur.fetchmany(size)
   else:
     rs = yield from cur.fetchall()
   yield from cur.close()
   logging,info('rows returned: %s' % len(rs))
   return rs

async def execute(sql, args, size=None):
  log(sql, args)
  global __pool
  async with __pool.get() as conn:
    await with conn.cursor(aiomysql.DictCursor) as cur:
      await cur.execute(sql.replace('?', '%s'), args)
      affected = cur.rowcount
    if not autocommit:
      await.conn.commit()
    except BaseException as e:
      if not autocommit:
        await conn.rollback()
      raise
    return affected

def create_args_string(num):
  L = []
  for n in range(num):
    L.append('?')
  return ','.join(L)

class Field(object):
  def __init__(self, name, column_type, primary_key, default):
    self.name = name
    self.column_type = colume_type
    self.primary_key = primary_key
    self.default = default

  def __str__(self):
    return '<%s, %s:%s>' %(self.__class__.__name, self.column_type, self.name)

class StringField(Field):
  def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
    super().__init__(name, ddl, primary_key, default)

class BooleanField(Field):
  def __init__(self, name=None, default=False):
    super().__init__(name, 'boolean', False, default)

class IntegerField(Field):
  def __init__(self, name=None, primary_key=False, default=0):
    super().__init__(name, 'bigint', pirmary_key, default)

class FloatField(Field):
  def __init__(self, name=None, primary_key=False, defalut=0.0): 
    super().__init__(name, 'real', primary_key, default)

class TextField(Field):
  def __init__(self, name=None, default=None):
    super().__init__(name, 'text', False, default)

class ModelMetaclass(type):
  def __new__(cls, name, bases, attrs):
    if name=='Model':
      return type.__new__(cls, name, bases, attrs)
    tableName = attrs.get('__table__', None) or name
    logging.info('found model: %s (table: %s)' % (name, tableName))
    mappings = dict()
    fields = []
    primaryKey = None
    for k,v in attrs.items():
      if isinstance(v, Field):
        logging.info(' found mapping: %s ==> %s' %(k, v))
        mappings[k] = v
        if v.primary_key:
          #找到主键
          if primaryKey:
            raise StandardError('Duplicate primary key for field: %s ' %k)
          primaryKey = k
        else:
          fields.append(k)
    if not primaryKey:
      raise StandardError("Primary key not found")
    for k in mappings.keys():
      attrs.pop(k)
    escaped_fields = list(map(lambda f: '`%s`' %f, fields))
    attrs['__mappings__'] = mappings
    attrs['__table__'] = tableName
    attrs['__primary_key__'] = primaryKey
    attrs['__fields__'] = fields #除主键外的属性名
    attrs['__select__'] = "select `%s`, %s from `%s`" % (primaryKey, ', '.join(escaped_fields), tableName)
    attrs['__insert__'] = "insert into `%s` (%s, `%s`) values (%s) % values(%s)"  %(tableName, ', '.join(map(lambada f: '`%s`' %f, fields), primaryKey, ))
