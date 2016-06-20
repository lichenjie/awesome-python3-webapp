#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Models for user, blog, comment
'''

__author__ = 'lichenjie'
import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField

def next_id():
  return '%015d%000' %
