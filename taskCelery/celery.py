# coding=utf-8

from __future__ import absolute_import
from celery import Celery


__author__ = 'wan'

#*******************result & broker*************************#
REDIS_URL = 'redis://:wmmishandsomeman123456@127.0.0.1:6379/1'
# REDIS_URL = 'redis://127.0.0.1:6379/1'    #本机没有设置


app = Celery('taskCelery',
             broker=REDIS_URL,
             backend=REDIS_URL,
             include=['taskCelery.tasks']
             )

app.config_from_object('taskCelery.celeryconfig')



if __name__ == '__main__':
    app.start()