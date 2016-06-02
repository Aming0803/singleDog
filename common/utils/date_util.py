# -*- coding:utf-8 -*-
from __future__ import absolute_import

import datetime
import time


def get_now(model="%Y-%m-%d %H:%M:%S"):
    """
    获取当前时间 %Y-%m-%d %H:%M:%S
    :return:
    """
    return datetime.datetime.now().strftime(model)


def get_time_stamp():
    """
    时间戳
    :return:
    """
    return int(time.time())


def date_add(day_num):
    now_time = datetime.datetime.now()
    if day_num:
        day_num = int(day_num)
        return now_time + datetime.timedelta(day_num)
    return now_time


def timeToStamp(value):
    """
     datetime转换成时间戳格式
    :param value:
    :return:
    """
    if not value:
        return int(time.time())

    timestamp = time.mktime(value.timetuple())

    return int(timestamp)


def timestamp2str(value):
    """
    时间戳转为字符串格式
    :param value:
    :return:
    """
    if not value:
        return ""

    t = time.localtime(value)
    return time.strftime("%Y-%m-%d %H:%M:%S", t)


def timeFromStr(value, model="%Y-%m-%d %H:%M:%S"):
    """
    字符串%Y-%m-%d %H:%M:%S->datetime
    :param value:
    :return:
    """
    if not value:
        return ''

    return datetime.datetime.strptime(value, model)


def get_timestamp_str():
    return "%0.f" % (time.time() * 1000)


def get_time_section(hour=15, minute=30, second=0):
    """
    获取每天无库存的时间区段
    :return:
    """
    now_day = datetime.datetime.now()
    before_day = now_day + datetime.timedelta(days=-1)

    start_time = before_day.replace(hour=hour, minute=minute, second=second)
    end_time = now_day.replace(hour=hour, minute=minute, second=second)

    return (start_time, end_time)


def get_section_time_by_params(start_time="", num=0):
    """
    根据时间和时间间隔获取另一时间
    :param start_time:datetime
    :param num:
    :return:
    """
    if not start_time:
        return False, "时间参数不能为空"
    else:
        end_time = start_time + datetime.timedelta(days=num)
        return True, end_time

def get_part_time(timestamp, num=3):
    """
    :param timestamp:时间戳
    :param num:区间段
    :return:
    """
    if not timestamp:
        return ""

    date_time_str = timestamp2str(timestamp)
    date_time = timeFromStr(date_time_str)

    end_time = date_time + datetime.timedelta(days=num)
    return date_time, end_time



