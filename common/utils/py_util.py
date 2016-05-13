# coding=utf-8
__author__ = 'wan'

import time
from string import Template


def remove_same_from_2_list(origin_list, target_list):
    """
    从origin_list去除target_list重复值
    :param origin_list:
    :param target_list:
    :return:
    """
    if not origin_list:
        return []

    if not target_list:
        return origin_list

    for val in target_list:
        if val in origin_list:
            origin_list.remove(val)

    return origin_list


def union_by_same(my_list):
    """
    合并相同的元祖
    :param my_list:
    :return:
    """
    if not my_list:
        return None

    middle = {}
    for data in my_list:
        key = data[0]
        val = data[-1]

        if middle.has_key(key):
            middle[key] += val
        else:
            middle[key] = val

    return middle


def create_order_id():
    return '%.f' % (time.time() * 1000)


def create_notify_id():
    return '%.f' % (time.time() * 1000000)


def sort_list_by_asc(data_list):
    """
    排序
    :param data_list:
    :return:
    """
    if not data_list:
        return None

    for origin_val in data_list[::-1]:
        target_list = data_list[0:-1]
        for target_val in target_list[::-1]:
            if origin_val < target_val:
                origin_index = data_list.index(origin_val)
                target_index = data_list.index(target_val)
                data_list[origin_index], data_list[target_index] = target_val, origin_val
            else:
                continue
    return data_list












if __name__ == '__main__':
    test_str = Template("""
        $name1: $age1,
        $name2: $age2,
    """)

    my_list = [6, 5, 7, 3, 1, 8, 2, 10, 4]
    time_list = [u'2016-03-28', u'2016-03-14', u'2016-03-13', u'2016-03-21', u'2016-05-02', u'2016-04-02']
    print sorted(time_list)
    print sort_list_by_asc(time_list)

    # print create_order_id()