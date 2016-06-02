#coding=utf-8
__author__ = 'wan'

from base_model import Base
from sqlalchemy.sql.functions import now
from sqlalchemy import Column, Integer, String, DateTime, Boolean, TEXT


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
    subscribe_time = Column(Integer, nullable=False, doc="关注时间戳")

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


class WXReplyDO(Base):
    """
    微信常用配置项
    """
    __tablename__ = "pm_wx_reply"

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
    __tablename__ = "pm_wx_image"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    source = Column(String(128), nullable=False, doc="原图片名称")
    source_path = Column(String(128), nullable=False, doc="原图片路径")
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
    category = Column(Integer, nullable=False, doc="素材类别", default=1)  #1.临时素材;2.永久素材，3.群发消息内的图文，视频上传
    source = Column(String(64), nullable=False, doc="原文件")
    is_expire = Column(Boolean, nullable=False, default=0, doc="是否过期")
    expire_time = Column(DateTime, nullable=True, doc="过期时间")
    url = Column(String(128), nullable=True, doc="新增图片永久素材返回URL")

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


class WXArticleDO(Base):
    """
    图文素材 文章列表
    """
    __tablename__ = 'pm_wx_article'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String(128), nullable=False, doc="标题")
    thumb_media_id = Column(String(128), nullable=False, doc="图文消息的封面图片素材id")   #（必须是永久mediaID）
    author = Column(String(32), nullable=False, doc="作者")
    digest = Column(String(256), nullable=True, doc="图文消息的摘要，仅有单图文消息才有摘要，多图文此处为空")
    show_cover_pic = Column(Integer, nullable=False, doc="是否显示封面", default=1)  #，0为false，即不显示，1为true，即显示
    content = Column(TEXT, nullable=False, doc="图文消息的具体内容") #，支持HTML标签，必须少于2万字符，小于1M，且此处会去除JS
    content_source_url = Column(String(128), nullable=False, doc="图文消息的原文地址")   #即点击“阅读原文”后的URL

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

    def convert_to_dict(self, excludes):
        """
        转换为字典
        :param excludes:排除字段列表
        :return:
        """
        if not excludes or not isinstance(excludes, list):
            excludes = ['gmt_created', 'gmt_modified', 'deleted']

        d = {}
        for field in WXArticleDO.__table__.columns:
            column_name = field.name
            if column_name in excludes:
                continue
            else:
                d.update({column_name: getattr(self, column_name)})

        return d


class WXMessageRecordDO(Base):
    """
    群发消息返回的纪录
    """
    __tablename__ = 'pm_wx_message_record'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    content = Column(String(128), nullable=False, doc="发送的内容")  #可以是文本,图文等
    type = Column(String(32), nullable=False, doc="发送内容的类型")
    msg_id = Column(Integer, nullable=False, doc="消息发送任务的ID")
    msg_data_id = Column(Integer, nullable=True, doc="消息的数据ID")     #该字段只有在群发图文消息时，才会出现
    status = Column(String(32), nullable=True, doc="群发的结构")     #为“send success”或“send fail”或“err(num)”
    total_count = Column(Integer, nullable=True, doc="ag_id下粉丝数,或者openid_list中的粉丝数")
    filter_count = Column(Integer, nullable=True, doc="过滤")     #(过滤是指特定地区、性别的过滤、用户设置拒收的过滤，用户接收已超4条的过滤）后，准备发送的粉丝数，原则上，FilterCount = SentCount + ErrorCount
    send_count = Column(Integer, nullable=True, doc="发送成功的数量")
    error_count = Column(Integer, nullable=True, doc="发送失败的粉丝数")

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