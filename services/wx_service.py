#coding=utf-8
__author__ = 'wan'

from connect_db.sql_conn import SQL_DB
from models.wx_model import (
    WXUserDO, WXReplyDO, WXMediaDO, WXImageUploadDO, WXMenuDO, WXArticleDO, WXMessageRecordDO
)
from common.utils.query_util import SimpleQuery
from common.utils.function_wrap import add_update_time
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

    @add_update_time
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

        menu_list = list_query.order_by(self._model.parent_id, self._model.gmt_created.desc()).slice(simple_query.start_row, simple_query.end_row).all()
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

        for key, val in kwargs.iteritems():
            if val:
                if key == "tagid_list":
                    val = ','.join(val)
                    setattr(user_do, "tag_list", val)
                else:
                    setattr(user_do, key, val)

        try:
            self.db.add(user_do)
            self.db.commit()
            return True, "创建成功"

        except Exception:
            self.db.rollback()
            return False, "创建失败"

    @add_update_time
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
            if val:
                if key == "tagid_list":
                    val = ','.join(val)
                    setattr(user, "tag_list", val)
                else:
                    setattr(user, key, val)

        try:
            self.db.commit()
            return True, "更新成功"

        except Exception:
            self.db.rollback()
            return False, "更新失败"

    def handle_user_by_subscribe_event(self, openid, **kwargs):
        """
        处理订阅事件
        :param openid:
        :param kwargs:
        :return:
        """
        user = self.get_user_by_openid(openid)
        if not user:
            success, msg = self.create_user_by_resp_data(**kwargs)
        else:
            kwargs.pop("openid")
            success, msg = self.update_wx_info_by_openid(openid, **kwargs)

        return success, msg

    def get_all_subscribe_user_list(self):
        """
        获取所有user
        :return:
        """
        return self.db.query(self._model).filter(self._model.deleted == 0, self._model.subscribe == 1).all()


class WXReplyService(object):

    _model = WXReplyDO

    def __init__(self):
        """
        微信配置服务
        比如回复等
        :return:
        """
        self.db = SQL_DB

    def get_reply_list_by_page(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        page_no = int(kwargs.get("page_no"))
        page_size = int(kwargs.get("page_size"))
        simple_query = SimpleQuery(page_no=page_no, page_size=page_size)

        list_query = self.db.query(self._model).filter(self._model.deleted == 0)
        count_query = self.db.query(func.count(self._model.id)).filter(self._model.deleted == 0)

        reply_list = list_query.order_by(self._model.gmt_created.desc()).slice(simple_query.start_row, simple_query.end_row).all()
        count = count_query.scalar()
        return reply_list, count

    def get_reply_by_id(self, reply_id):
        """
        :param reply_id:
        :return:
        """
        return self.db.query(self._model).filter(self._model.deleted == 0, self._model.id == reply_id).first()

    @add_update_time
    def update_reply_by_id(self, reply_id, **kwargs):
        """
        :param reply_id:
        :return:
        """
        reply = self.get_reply_by_id(reply_id)
        if not reply:
            return False, "数据异常,对象不存在"

        for key, val in kwargs.iteritems():
            if val:
                setattr(reply, key, val)

        try:
            self.db.commit()
            return True, "更新成功"
        except Exception:
            self.db.rollback()
            return False, "更新失败"

    def create_reply_by_params(self, **kwargs):
        """
        create
        :param kwargs:
        :return:
        """
        reply_do = self._model()

        for key, val in kwargs.iteritems():
            if val:
                setattr(reply_do, key, val)

        try:
            self.db.add(reply_do)
            self.db.commit()
            return True, "创建成功"
        except Exception:
            self.db.rollback()
            return False, "创建失败"

    def get_reply_by_key(self, key):
        """
        根据key获取
        :param key:
        :return:
        """
        return self.db.query(self._model).filter(self._model.deleted == 0, self._model.key == key).first()



class WXUploadImgService(object):

    _model = WXImageUploadDO

    def __init__(self):
        """
        微信上传图片
        :return:
        """
        self.db = SQL_DB

    def create_upload_img_by_params(self, **kwargs):
        """
        创建上传成功后的图片信息
        :param kwargs:
        :return:
        """
        img_do = self._model()

        for key, val in kwargs.iteritems():
            if val:
                setattr(img_do, key, val)

        try:
            self.db.add(img_do)
            self.db.commit()
            return True, "创建成功"

        except Exception:
            self.db.rollback()
            return False, "创建失败"

    def get_upload_img_list_by_page(self, **kwargs):
        """
        获取列表
        :param kwargs:
        :return:
        """
        page_no = int(kwargs.get("page_no"))
        page_size = int(kwargs.get("page_size"))
        simple_query = SimpleQuery(page_no=page_no, page_size=page_size)

        list_query = self.db.query(self._model).filter(self._model.deleted == 0)
        count_query = self.db.query(func.count(self._model.id)).filter(self._model.deleted == 0)

        reply_list = list_query.order_by(self._model.gmt_created.desc()).slice(simple_query.start_row, simple_query.end_row).all()
        count = count_query.scalar()
        return reply_list, count

    def get_upload_img_by_id(self, img_id):
        """
        get by id
        :param img_id:
        :return:
        """
        return self.db.query(self._model).filter(self._model.deleted == 0, self._model.id == img_id).first()


class WXArticleService(object):

    _model = WXArticleDO

    def __init__(self):
        """
        图文 文章服务
        :return:
        """
        self.db = SQL_DB

    def get_article_list_by_page(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        page_no = int(kwargs.get("page_no"))
        page_size = int(kwargs.get("page_size"))
        simple_query = SimpleQuery(page_no=page_no, page_size=page_size)

        list_query = self.db.query(self._model).filter(self._model.deleted == 0)
        count_query = self.db.query(func.count(self._model.id)).filter(self._model.deleted == 0)

        reply_list = list_query.order_by(self._model.gmt_created.desc()).slice(simple_query.start_row, simple_query.end_row).all()
        count = count_query.scalar()
        return reply_list, count

    def get_article_list(self):
        """
        上传图文时候获取所有的文章
        :return:
        """
        return self.db.query(self._model).filter(self._model.deleted == 0).all()

    def create_article_by_params(self, **kwargs):
        """
        创建
        :param kwargs:
        :return:
        """
        article_do = self._model()

        for key, val in kwargs.iteritems():
            if val:
                setattr(article_do, key, val)

        try:
            self.db.add(article_do)
            self.db.commit()
            return True, "创建成功"

        except Exception:
            self.db.rollback()
            return False, "创建失败"

    def get_article_by_article_id(self, id):
        """
        :param id:
        :return:
        """
        return self.db.query(self._model).filter(self._model.deleted == 0, self._model.id == id).first()

    def get_article_title_by_article_id(self, article_id):
        """
        获取标题
        :param article_id:
        :return:
        """
        article = self.get_article_by_article_id(article_id)
        title = article.title if article else ""
        return title


class WXMediaService(object):

    _model = WXMediaDO

    def __init__(self):
        """
        微信素材
        :return:
        """
        self.db = SQL_DB

    def get_permanent_media_list(self):
        """
        获取永久素材
        :return:
        """
        return self.db.query(self._model).filter(self._model.deleted == 0, self._model.category == 2).all()

    def get_permanent_thumb_media_list(self):
        """
        获取永久缩略图素材
        :return:
        """
        return self.db.query(self._model).filter(self._model.deleted == 0, self._model.category == 2, self._model.type == 'thumb').all()

    def create_media_by_params(self, **kwargs):
        """
        保存素材
        :param kwargs:
        :return:
        """
        media_do = self._model()

        for key, val in kwargs.iteritems():
            if val:
                setattr(media_do, key, val)

        try:
            self.db.add(media_do)
            self.db.commit()
            return True, "创建成功"

        except Exception:
            self.db.rollback()
            return False, "创建失败"

    def get_admin_media_list_by_page(self, **kwargs):
        """
        素材后台分页列表
        :param kwargs:
        :return:
        """
        page_no = int(kwargs.get("page_no"))
        page_size = int(kwargs.get("page_size"))
        simple_query = SimpleQuery(page_no=page_no, page_size=page_size)

        list_query = self.db.query(self._model).filter(self._model.deleted == 0)
        count_query = self.db.query(func.count(self._model.id)).filter(self._model.deleted == 0)

        reply_list = list_query.order_by(self._model.gmt_created.desc()).slice(simple_query.start_row, simple_query.end_row).all()
        count = count_query.scalar()
        return reply_list, count

    def get_message_news_media_list(self):
        """
        获取群发接口中上传的图文素材列表
        :return:
        """
        return self.db.query(self._model).filter(self._model.deleted == 0, self._model.category == 3).all()


class WXMessageRecordService(object):

    _model = WXMessageRecordDO

    def __init__(self):
        """
        群发消息纪录
        :return:
        """
        self.db = SQL_DB

    def get_wx_message_record_do_by_msg_id(self, msg_id):
        """
        get by msg id
        :param msg_id:
        :return:
        """
        return self.db.query(self._model).filter(self._model.deleted == 0, self._model.msg_id == msg_id).first()

    def create_wx_message_record_by_params(self, **kwargs):
        """
        创建
        :param kwargs:
        :return:
        """
        message_do = self._model()

        for key, val in kwargs.iteritems():
            if val:
                setattr(message_do, key, val)

        try:
            self.db.add(message_do)
            self.db.commit()
            return True, "创建成功"

        except Exception:
            self.db.rollback()
            return False, "创建失败"

    @add_update_time
    def update_wx_message_record_by_msg_id(self, msg_id, **kwargs):
        """
        更新
        :param msg_id:
        :param kwargs:
        :return:
        """
        msg = self.get_wx_message_record_do_by_msg_id(msg_id)

        for key, val in kwargs.iteritems():
            if val:
                setattr(msg, key, val)

        try:
            self.db.commit()
            return True, "更新成功"

        except Exception:
            self.db.rollback()
            return False, "更新失败"