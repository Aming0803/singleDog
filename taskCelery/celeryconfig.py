# coding=utf-8
from __future__ import absolute_import
from celery.schedules import crontab
from kombu import Queue, Exchange

__author__ = 'wan'

#time and date
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True

#CELERY_ANNOTATIONS  注释,比如某个任务多长时间执行一次等等
# CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '30/m'}}

###serializer
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']

#不会用到结果
# CELERY_IGNORE_RESULT = True

####custom queue and route
default_exchange = Exchange('default', type='direct')

#新建不同的queue
CELERY_QUEUES = (
    Queue('default', default_exchange, routing_key='default'),
)

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'

