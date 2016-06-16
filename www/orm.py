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



