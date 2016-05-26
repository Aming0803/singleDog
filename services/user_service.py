#coding=utf-8
__author__ = 'wan'

from connect_db.sql_conn import SQL_DB
from models.user_model import AdminUserDO



class AdminUserService(object):

    _model = AdminUserDO

    def __init__(self):
        """
        后台用户管理服务
        :return:
        """
        self.db = SQL_DB

    def get_admin_user_by_username_and_password(self, username, password):
        """
        根据用户名和密码获取用户
        :param username:
        :param password:
        :return:
        """
        return self.db.query(self._model).filter(self._model.deleted == 0, self._model.username == username, self._model.password == password).first()

    def create_admin_user_by_params(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        user_do = self._model()
        for key, val in kwargs.iteritems():
            setattr(user_do, key, val)

        try:
            self.db.add(user_do)
            self.db.commit()
            return True, "创建完成"

        except Exception:
            self.db.rollback()
            return False, "创建失败"