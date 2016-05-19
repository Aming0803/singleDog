#coding=utf-8
__author__ = 'wan'

from connect_db.sql_conn import SQL_DB


class WXMenuService(object):

    def __init__(self):
        """
        微信菜单服务
        :return:
        """
        self.db = SQL_DB


class WXUserService(object):

    def __init__(self):
        """
        微信用户
        :return:
        """
        self.db = SQL_DB