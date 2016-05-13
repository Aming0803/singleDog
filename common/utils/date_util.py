# -*- coding:utf-8 -*-
from __future__ import absolute_import

import datetime
import time
from time import strftime, localtime
from common.common_settings import FLOWER_ORDER_END_HOUR, FLOWER_ORDER_END_MIN, FLOWER_ORDER_END_SECOND

def get_now():
    """
    获取当前时间 %Y-%m-%d %H:%M:%S
    :return:
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_now_date():
    """
    YYYY-mm-dd
    :return:
    """
    return datetime.datetime.now().strftime('%Y-%m-%d')

def get_time_stamp():
    """
    时间戳
    :return:
    """
    return int(time.time())


def datetime2date(dt):
    """
    根据datetime获取date
    :param dt:
    :return:
    """
    return dt.lstrip().split(' ')[0]


def yyyydddddatetime():
    '''''
    get datetime,format="YYYY-MM-DD HH:MM:SS"
    '''
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


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


def time2str(d):
    """
    时间转化成字符串格式‘Y-m-d H:M:S’
    :param d:
    :return:
    """
    if not d:
        return ''

    # if not isinstance(d, datetime):
    #     return d

    return d.strftime("%Y-%m-%d %H:%M:%S")


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


def get_order_cancel_section(num=5):
    """
    获取取消订单的时间段，默认是当前时间到前4天
    :param num:
    :return:
    """
    now_day = datetime.datetime.now()
    before_day = now_day + datetime.timedelta(days=-num)

    start_time = time2str(before_day)
    end_time = time2str(now_day)
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


def get_query_section(num=1):
    """
    :param num:
    :return:
    """
    return get_order_cancel_section(num)


def get_bd_query_time(num=2):
    """
    百度订单查询日期
    :param num:
    :return:
    """
    now_day = datetime.datetime.now()
    before_day = now_day + datetime.timedelta(days=-num)

    return before_day, now_day

def get_order_task_time(create_time, num, task_date, end_date, cycle="week"):
    """
    获取订单配送任务时间
    在结单日和下个结单日之间，则在下周配送，否则下下周配送
    :param create_time:拉单时间
    :param num:拆分次数
    :param task_date:任务时间,指星期一(0), 星期二(1).....
    :return:
    """
    now_time = datetime.datetime.now()
    now_day_num = now_time.weekday()

    #ps.需求更改create_time从订单拉取更改为订单创建时间

    if cycle == "week":

        end_time = now_time + datetime.timedelta(days=(end_date-now_day_num))
        end_time = end_time.replace(hour=FLOWER_ORDER_END_HOUR, minute=FLOWER_ORDER_END_MIN, second=FLOWER_ORDER_END_SECOND)

        #ps.拉单时间小于结单日期,则在下周配送，反之，则在下下周配送
        if create_time <= end_time:
            result = now_time + datetime.timedelta(days=(task_date-now_day_num), weeks=num)
        else:
            result = now_time + datetime.timedelta(days=(task_date-now_day_num), weeks=num+1)

    else:
        #ps.cycle == "month", task_date = 01,02,----31, end_date=01,02,---31
        end_time = now_time.replace(day=end_date, hour=FLOWER_ORDER_END_HOUR, minute=FLOWER_ORDER_END_MIN, second=FLOWER_ORDER_END_SECOND)

        now_month_num = now_time.month
        if create_time <= end_time:
            result = now_time.replace(month=now_month_num+num, day=task_date)
        else:
            result = now_time.replace(month=now_month_num+num+1, day=task_date)

    return result.strftime("%Y-%m-%d")


def get_order_task_time_v2(order_create_time, num, task_date, end_date, cycle="week"):
    """
    获取订单配送任务时间
    在结单日和下个结单日之间，则在下周配送，否则下下周配送
    :param create_time:拉单时间 字符串
    :param num:拆分次数
    :param task_date:任务时间,指星期一(0), 星期二(1).....
    :return:
    """

    #ps.需求更改create_time从订单拉取更改为订单创建时间
    #ps.注意为了满足历史订单的拆分，所以now_time应该是创建订单所在的日前。
    create_time = timeFromStr(order_create_time)
    create_day_num = create_time.weekday()

    now_time, now_day_num = create_time, create_day_num

    if cycle == "week":

        end_time = now_time + datetime.timedelta(days=(end_date-now_day_num))
        end_time = end_time.replace(hour=FLOWER_ORDER_END_HOUR, minute=FLOWER_ORDER_END_MIN, second=FLOWER_ORDER_END_SECOND)

        #ps.拉单时间小于结单日期,则在下周配送，反之，则在下下周配送
        if create_time <= end_time:
            result = now_time + datetime.timedelta(days=(task_date-now_day_num), weeks=num)
        else:
            result = now_time + datetime.timedelta(days=(task_date-now_day_num), weeks=num+1)

    else:
        #ps.cycle == "month", task_date = 01,02,----31, end_date=01,02,---31
        end_time = now_time.replace(day=end_date, hour=FLOWER_ORDER_END_HOUR, minute=FLOWER_ORDER_END_MIN, second=FLOWER_ORDER_END_SECOND)

        now_month_num = now_time.month
        if create_time <= end_time:
            result = now_time.replace(month=now_month_num+num, day=task_date)
        else:
            result = now_time.replace(month=now_month_num+num+1, day=task_date)

    return result.strftime("%Y-%m-%d")


def get_end_time_with_set_flower():
    """
    获取鲜花设置的起始和结束时间
    本周一至周日晚上
    :return:
    """
    now_time = datetime.datetime.now()
    now_day_num = now_time.weekday()

    #ps.星期日晚上
    end_day_num = 6
    end_time = now_time + datetime.timedelta(days=end_day_num-now_day_num, hours=23, minutes=59, seconds=59)

    return end_time













if __name__ == '__main__':
    # t = timeFromStr("2016-02-11", "%Y-%m-%d")
    # print t.__class__.__name__
    date_time_str = "2016-04-08 12:00:00"
    date_time = timeFromStr(date_time_str)
    print timeToStamp(date_time)
