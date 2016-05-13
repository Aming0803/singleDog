#coding=utf-8
__author__ = 'wan'

from tornado.web import authenticated
from common.handlers.admin_base_handler import AdminBaseHandler


class IndexHandler(AdminBaseHandler):

    def get(self):
        return self.render("index.html")
