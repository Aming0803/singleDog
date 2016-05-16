#coding=utf-8
__author__ = 'wan'


from tornado.web import RequestHandler


class AppBaseHandler(RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie('wx_app_user_id', "")

    def get_current_user_name(self):
        return self.get_secure_cookie('wx_app_user_name', "")

    @property
    def current_user_name(self):
        """
        用户名称
        :return:
        """
        return self.get_current_user_name()