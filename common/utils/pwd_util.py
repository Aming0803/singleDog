# -*- coding:utf-8 -*-
import hashlib






def create_md5(args):
    """
    md5加密
    :param args:
    :return:
    """
    md5_constructor = hashlib.md5
    return md5_constructor(args).hexdigest()


def create_sha1(val):
    """
    sha1加密
    :param val:
    :return:
    """
    if not val:
        return False

    return hashlib.sha1(val).hexdigest()