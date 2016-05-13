# coding=utf-8
__author__ = 'wan'

import datetime
from common.utils.date_util import time2str


def row2dict(row, model):
    """
    row convert to dict
    :param row:
    :return:
    """
    d = {}
    if isinstance(row, model):
        for column in row.__table__.columns:
            field = str(column.name)
            if field not in ['gmt_created','gmt_modified','deleted']:
                val = getattr(row, column.name)
                if not val:
                    continue
                else:
                    if field.endswith('time'):
                        d.update({field: time2str(val)})
                    else:
                        d.update({field:val})
    return d


def wyOrderRow2Dict(row, model):
    """
    row convert to dict
    :param row:
    :return:
    """
    d = {}
    if isinstance(row, model):
        for column in row.__table__.columns:
            field = str(column.name)
            if field not in ['gmt_created','gmt_modified','deleted']:
                val = getattr(row, column.name)
                if not val:
                    continue
                else:
                    d.update({field:val})
    return d

def wmsModelObj2Dict(obj):
    """
    wms 对象转换为字典
    :param obj:
    :return:
    """
    d = {}
    field_list = obj.get_model_fields()
    for field in field_list:
        value = getattr(obj, field)
        if value:
            d.update({field: value})
        else:
            continue

    return d

def xcfModelObj2Dict(obj):
    """
    wms 对象转换为字典
    :param obj:
    :return:
    """
    d = {}
    field_list = obj.get_model_fields()
    for field in field_list:
        value = getattr(obj, field)
        if value:
            d.update({field: value})
        else:
            continue

    return d


def modelObj2Dict(obj):
    """
    wms 对象转换为字典
    :param obj:
    :return:
    """
    d = {}
    field_list = obj.get_model_fields()
    for field in field_list:
        value = getattr(obj, field)
        if value:
            d.update({field: value})
        else:
            continue

    return d