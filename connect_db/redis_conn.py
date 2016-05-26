#coding=utf-8
__author__ = 'wan'

import redis
from common.utils.function_wrap import singleton
from config import redis_server_env, redis_server_passwd, redis_server_port

@singleton
class RedisManger(object):
    def __init__(self):
        pass

    @property
    def conn(self):
        if not hasattr(self, '_redis_conn'):
            self._redis_conn = self.redis_conn()
        return self._redis_conn

    @conn.setter
    def conn(self, val):
        self._redis_conn = val


    def redis_conn(self):
        pool = redis.ConnectionPool(host=redis_server_env,port=redis_server_port, max_connections=1024)
        return redis.Redis(connection_pool = pool)


REDIS_DB = RedisManger().conn



