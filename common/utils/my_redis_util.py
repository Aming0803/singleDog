# coding=utf-8
__author__ = 'wan'



def push_value_to_list(redis_db, name, value):
    """
    保存值到列表
    :param redis_db:
    :param name:
    :param value:
    :return:
    """
    if not redis_db or not name or not value:
        return False, '参数不能为空'

    my_list = redis_db.lrange(name, 0, -1)
    if value in my_list:
        pass
    else:
        redis_db.lpush(name, value)

    return True, '添加成功'


def delete_value_to_list(redis_db, name, value):
    """
    保存值到列表
    :param redis_db:
    :param name:
    :param value:
    :return:
    """
    if not redis_db or not name or not value:
        return False, '参数不能为空'

    my_list = redis_db.lrange(name, 0, -1)
    if value in my_list:
        redis_db.lrem(name, value)
    else:
        pass

    return True, '删除成功'

def delete_value_from_hash(redis_db, name, key):
    """
    :param redis_db:
    :param name:
    :return:
    """
    if not redis_db or not name or not key:
        return False, '参数不能为空'

    if redis_db.hexists(name, key):
        redis_db.hdel(name, key)
    else:
        pass

    return True, ""

def get_except_info(redis_db, name, key):
    """
    从异常redis中获取异常信息
    :param redis_db:
    :param name:
    :param key:
    :return:
    """
    if not redis_db or not name or not key:
        return False, "参数不能为空"

    if redis_db.hexists(name, key):
        return True, redis_db.hget(name, key)
    else:
        return False, ""

def hset_value(redis_db, name, key, value):
    """
    hash set value类似字典
    :param redis_db:
    :param name:
    :param key:
    :param value:
    :return:
    """
    if not redis_db or not name or not key or not value:
        return False, "参数不能为空"

    is_exist = redis_db.hexists(name, key)
    if is_exist:
        pass
    else:
        redis_db.hset(name, key, value)

    return True, ""

