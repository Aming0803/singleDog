#coding=utf-8
__author__ = 'wan'

from connect_db.sql_conn import SQL_DB
from models.wx_model import WXUserDO, WXConfigDO, WXMediaDO, WXImageUploadDO, WXMenuDO
from common.utils.query_util import SimpleQuery
from sqlalchemy import func

class WXMenuService(object):

    _model = WXMenuDO

    def __init__(self):
        """
        微信菜单服务
        :return:
        """
        self.db = SQL_DB

    def get_menu_by_id(self, menu_id):
        """
        get by object id
        :param menu_id:
        :return:
        """
        return self.db.query(self._model).filter(self._model.deleted == 0, self._model.id == menu_id).first()

    def get_parent_menu_list(self):
        """
        获取一级菜单列表
        :return:
        """
        return self.db.query(self._model).filter(self._model.deleted == 0, self._model.category == 1).all()

    def get_child_menu_list(self, menu_id):
        """
        获取所有子菜单
        :param menu_id:
        :return:
        """
        return self.db.query(self._model).filter(self._model.deleted == 0, self._model.category == 2, self._model.parent_id == menu_id).all()

    def update_menu_info_by_id(self, menu_id, **kwargs):
        """
        根据菜单id更新
        :param menu_id:
        :return:
        """
        menu = self.get_menu_by_id(menu_id)
        for key, val in kwargs.iteritems():
            if val:
                setattr(menu, key, val)

        try:
            self.db.commit()
            return True, "更新成功"
        except Exception:
            self.db.rollback()
            return False, "更新失败"

    def create_menu_by_params(self, **kwargs):
        """
        创建
        :param kwargs:
        :return:
        """
        menu_do = self._model()
        for key, val in kwargs.iteritems():
            if val:
                setattr(menu_do, key, val)
        try:
            self.db.add(menu_do)
            if kwargs.get("category") == 1:
                menu_do.parent_id = 0

            self.db.commit()
            return True, menu_do.id

        except Exception:
            self.db.rollback()
            return False, "创建失败"

    def get_menu_list_by_page(self, **kwargs):
        """
        后台分页
        :param kwargs:
        :return:总页数和菜单列表
        """
        page_no = int(kwargs.get("page_no"))
        page_size = int(kwargs.get("page_size"))
        simple_query = SimpleQuery(page_no=page_no, page_size=page_size)

        list_query = self.db.query(self._model).filter(self._model.deleted == 0)
        count_query = self.db.query(func.count(self._model.id)).filter(self._model.deleted == 0)

        menu_list = list_query.order_by(self._model.parent_id).slice(simple_query.start_row, simple_query.end_row).all()
        count = count_query.scalar()
        return menu_list, count

    def get_active_parent_menu_list(self):
        """
        获取正在使用中的一级菜单
        :return:
        """
        return self.db.query(self._model).filter(self._model.deleted == 0, self._model.category == 1, self._model.is_active == 1).all()

    def get_active_child_menu_list(self, menu_id):
        """
        获取正在使用中的子菜单列表
        :return:
        """
        return self.db.query(self._model).filter(self._model.deleted == 0, self._model.category == 2, self._model.is_active == 1, self._model.parent_id == menu_id).all()


class WXUserService(object):

    _model = WXUserDO

    def __init__(self):
        """
        微信用户
        :return:
        """
        self.db = SQL_DB

    def get_user_by_openid(self, openid):
        """
        根据openid获取user
        :param openid:
        :return:
        """
        return self.db.query(WXUserDO).filter(WXUserDO.deleted == 0, WXUserDO.openid == openid).first()

    def create_user_by_resp_data(self, **kwargs):
        """
        根据返回数据保存用户
        :param kwargs:
        :return:
        """
        user_do = WXUserDO()

        for field in WXUserDO.get_model_fields():
            if field == "id":
                continue

            val = kwargs.get(field)
            if val:
                setattr(user_do, field, val)

        try:
            self.db.add(user_do)
            self.db.commit()
            return True, "创建成功"

        except Exception:
            self.db.rollback()
            return False, "创建失败"

    def update_wx_info_by_openid(self, openid, **kwargs):
        """
        :param openid:
        :param kwargs:
        :return:
        """
        user = self.get_user_by_openid(openid)
        if not user:
            return False, "用户不存在"

        for key, val in kwargs.iteritems():
            setattr(user, key, val)

        try:
            self.db.commit()
            return True, "更新成功"

        except Exception:
            self.db.rollback()
            return False, "更新失败"


class WXConfigService(object):

    _model = WXConfigDO

    def __init__(self):
        """
        微信配置服务
        :return:
        """
        self.db = SQL_DB