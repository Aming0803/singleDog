# -*- coding:utf-8 -*-
import hashlib
import os
from common.common_settings import USER_SECRET

__author__ = 'shenhai'






def create_md5(args):
    md5_constructor = hashlib.md5
    return md5_constructor(args).hexdigest()




def user_pwd_digest(passwd):
    """
    用户加密密码处理
    :param passwd:
    :return:
    """
    ttt=USER_SECRET + passwd
    return create_md5(ttt)



if __name__ == '__main__':
    # passwd = 'wan888'
    # print user_pwd_digest(passwd)
    key = "1450695025498"+ "d196371019e3bc82"
    print create_md5(key)