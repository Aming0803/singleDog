# coding=utf-8
__author__ = 'wan'

import datetime


#单列模式
def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


#给更新对象添加时间
def add_update_time(func):
    def _func(*args, **kwargs):
        now_d = datetime.datetime.now()
        kwargs.update({"gmt_modified": now_d})
        return func(*args, **kwargs)
    return _func