#coding=utf-8
__author__ = 'wan'


from tornado.web import RequestHandler


class AppBaseHandler(RequestHandler):

    def get_current_user(self):
        """
        override
        :return:
        """
        current_user_id = self.get_secure_cookie("wx_app_user_id")
        if not current_user_id:
            return ""
        return current_user_id

    def get_current_user_name(self):
        """
        current user name
        :return:
        """
        return self.get_secure_cookie('wx_app_user_name')

    @property
    def current_wx_app_user_name(self):
        """
        用户名称
        :return:
        """
        return self.get_current_user_name()

    @property
    def current_wx_app_user_id(self):
        """
        app user id
        :return:
        """
        if not hasattr(self, "_wx_app_user"):
            self._wx_app_user = self.get_current_user()
        return self._wx_app_user

    @current_wx_app_user_id.setter
    def current_wx_app_user_id(self, value):
        """
        :param value:
        :return:
        """
        self._wx_app_user = value