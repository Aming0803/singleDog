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
    value = Column(String(512), nullable=False, doc="对应的值")
    category = Column(Integer, nullable=False, doc="菜单级别")
    is_active = Column(Integer, nullable=False, doc="是否再使用中", default=1)    #0.未使用, 1.使用中

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
    groupid = Column(Integer, nullable=True, doc="用户所在的分组ID")


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


class WXConfigDO(Base):
    """
    微信常用配置项
    """
    __tablename__ = "pm_wx_config"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    key = Column(String(64), nullable=False, doc="关键值")
    reply_type = Column(String(32), nullable=False, doc="回复类型")
    content = Column(String(1000), nullable=False, doc="内容")

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


class WXImageUploadDO(Base):
    """
    微信图文消息中图片上传URL保存
    """
    __tablename__ = "pm_wx_image_url"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    source = Column(String(128), nullable=False, doc="原图片名称")
    url = Column(String(256), nullable=False, doc="上传后返回的URL")

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


class WXMediaDO(Base):
    """
    微信素材管理
    """
    __tablename__ = "pm_wx_media"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    type = Column(String(32), nullable=False, doc="返回类型")
    media_id = Column(String(128), nullable=False, doc="素材ID")
    created = Column(Integer, nullable=True, doc="媒体文件上传时间")

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