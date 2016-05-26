#coding=utf-8
__author__ = 'wan'

from common.handlers.admin_base_handler import AdminBaseHandler
from services.user_service import AdminUserService
from common.utils.pwd_util import create_md5
from common.utils.py_util import create_str_id
from common.utils.auth_util import admin_authenticated
from common.config import DOMAIN

import logging
import traceback
log = logging.getLogger(__file__)


class IndexHandler(AdminBaseHandler):

    @admin_authenticated
    def get(self):
        return self.render('index.html')


class AdminLoginHandler(AdminBaseHandler):

    _Template_Name = "login.html"

    def get(self):
        """
        后台管理登陆
        :return:
        """
        if self.current_user:
            return self.redirect('/')

        next_url = self.get_argument("next", "/")
        return self.render(self._Template_Name, msg="", next_url=next_url)

    def post(self):
        """
        后台管理登陆
        :return:
        """
        username = self.get_argument("username", "").strip()
        password = self.get_argument("password", "").strip()
        next_url = self.get_argument("next", "/")
        if not username or not password:
            return self.render(self._Template_Name, msg="用户名或密码不存在", next_url=next_url)

        admin_user_ser = AdminUserService()
        admin_user = admin_user_ser.get_admin_user_by_username_and_password(username, create_md5(password))
        if not admin_user:
            return self.render(self._Template_Name, msg="用户名或密码不正确", next_url=next_url)

        self.make_secure_cookie(admin_user.user_id, admin_user.username)

        return self.redirect(next_url)

    def make_secure_cookie(self, user_id, username):
        """
        生成session
        :return:
        """
        self.set_secure_cookie('wx_admin_user_id', user_id, domain=DOMAIN)
        self.set_secure_cookie('wx_admin_user_name', username, domain=DOMAIN)


class AdminUserRegisterHandler(AdminBaseHandler):

    _Template_Name = "register.html"

    def get(self):
        """
        注册页面跳转
        :return:
        """
        return self.render(self._Template_Name, msg="")

    def post(self):
        """
        注册用户
        :return:
        """
        username = self.get_argument("username", "").strip()
        password = self.get_argument("password", "").strip()
        email = self.get_argument("email", "").strip()
        telephone = self.get_argument("telephone", "").strip()

        if not username or not password or not email or not telephone:
            msg = "参数不能为空"
            return self.render(self._Template_Name, msg=msg)

        admin_user_ser = AdminUserService()
        password = create_md5(password)
        admin_user = admin_user_ser.get_admin_user_by_username_and_password(username, password)
        if admin_user:
            msg = "该账号已存在,请重新填写"
            return self.render(self._Template_Name, msg=msg)

        user_id = create_str_id()
        success, msg = admin_user_ser.create_admin_user_by_params(username=username, password=password, email=email,
                                                                  telephone=telephone, user_id=user_id)
        if not success:
            return self.render(self._Template_Name, msg=msg)
        else:
            self.make_secure_cookie(user_id, username)
            return self.redirect("/")


    def make_secure_cookie(self, user_id, username):
        """
        生成session
        :return:
        """
        self.set_secure_cookie('wx_admin_user_id', user_id, domain=DOMAIN)
        self.set_secure_cookie('wx_admin_user_name', username, domain=DOMAIN)


class AdminLogoutHandler(AdminBaseHandler):
    @admin_authenticated
    def get(self):
        """
        退出系统
        :return:
        """
        self.clear_admin_cookies()
        return self.redirect(self.get_login_url())

    def clear_admin_cookies(self):
        """
        清楚session
        :return:
        """
        self.clear_cookie("wx_admin_user_id")
        self.clear_cookie("wx_admin_user_name")





