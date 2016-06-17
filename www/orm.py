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
    super().__init__(name, 'boolen', False, default)

class IntegerField(Field):
  def __init__(self, name=None, default=False)
    super().__init__(name, '')

