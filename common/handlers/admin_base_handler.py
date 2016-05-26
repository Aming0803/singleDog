#coding=utf-8
__author__ = 'wan'


from tornado.web import RequestHandler



class AdminBaseHandler(RequestHandler):

    def get_current_user(self):
        current_user_id = self.get_secure_cookie("wx_admin_user_id")
        if not current_user_id:
            return ""
        return current_user_id

    def get_current_user_name(self):
        return self.get_secure_cookie('wx_admin_user_name')

    @property
    def current_wx_admin_user_name(self):
        """
        用户名称
        :return:
        """
        return self.get_current_user_name()

    @property
    def current_wx_admin_user_id(self):
        """
        当前后台用户
        :return:
        """
        if not hasattr(self, "_wx_admin_user"):
            self._wx_admin_user = self.get_current_user()
        return self._wx_admin_user

    @current_wx_admin_user_id.setter
    def current_wx_admin_user_id(self, value):
        """
        :param val:
        :return:
        """
        self._wx_admin_user = value

    def get_template_namespace(self):
        """
        扩展template
        :return:
        """
        namespace = super(AdminBaseHandler, self).get_template_namespace()
        namespace.update({"current_user_name": self.current_wx_admin_user_name})
        return namespace