#coding=utf-8
__author__ = 'wan'

from base_model import Base
from sqlalchemy.sql.functions import now
from sqlalchemy import Column, Integer, String, DateTime, Boolean


class WXMenuDO(Base):
    """
    微信自定义菜单
    """
    __tablename__ = "pm_wx_menu"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    parent_id = Column(Integer, nullable=False, doc="父菜单")
    name = Column(String(64), nullable=False, doc="菜单名字")
    menu_type = Column(String(128), nullable=False, doc="菜单类型")
    key = Column(String(128), nullable=True, doc="菜单KEY值，用于消息接口推送") #click等点击类型必须
    url = Column(String(1024), nullable=True, doc="网页链接，用户点击菜单可打开链接")    #view类型必须
    media_id = Column(String(128), nullable=True, doc="调用新增永久素材接口返回的合法")    #media_id类型和view_limited类型必须

    gmt_created = Column(DateTime, default=now())
    gmt_modified = Column(DateTime, default=now())
    deleted = Column(Boolean, nullable=False, default=0)

    @classmethod
    def get_model_fields(cls):
        """
        获取所有的字段，除了gmt_created，gmt_modified，deleted
        :return:
        """
        field_list = []
        for field in cls.__table__.columns:
            column_name = field.name
            if column_name in ['gmt_created', 'gmt_modified', 'deleted']:
                continue
            else:
                field_list.append(column_name)

        return field_list


class WXUserDO(Base):
    """
    微信用户
    """
    __tablename__ = "pm_wx_user"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    subscribe = Column(Integer, nullable=False, default=0, doc="用户是否订阅")    #0:非订阅,1:订阅
    openid = Column(String(128), nullable=False, doc="用户OPENID")
    nickname = Column(String(128), nullable=True, doc="用户昵称")
    sex = Column(Integer, nullable=True, doc="性别")  #用户的性别，值为1时是男性，值为2时是女性，值为0时是未知
    headimgurl = Column(Integer, nullable=True, doc="用户头像")
    unionid = Column(String(128), nullable=True)    #只有在用户将公众号绑定到微信开放平台帐号后，才会出现该字段
    city = Column(String(64), nullable=True, doc="城市")
    country = Column(String(64), nullable=True, doc="国家")
    province = Column(String(64), nullable=True, doc="省份")
    tag_list = Column(String(64), nullable=True, doc="用户标签列表")
    latitude = Column(String(32), nullable=True, doc="地理位置纬度")
    longitude = Column(String(32), nullable=True, doc="地理位置经度")

    gmt_created = Column(DateTime, default=now())
    gmt_modified = Column(DateTime, default=now())
    deleted = Column(Boolean, nullable=False, default=0)

    @classmethod
    def get_model_fields(cls):
        """
        获取所有的字段，除了gmt_created，gmt_modified，deleted
        :return:
        """
        field_list = []
        for field in cls.__table__.columns:
            column_name = field.name
            if column_name in ['gmt_created', 'gmt_modified', 'deleted']:
                continue
            else:
                field_list.append(column_name)

        return field_list