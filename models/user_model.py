#coding=utf-8
__author__ = 'wan'

from base_model import Base
from sqlalchemy.sql.functions import now
from sqlalchemy import Column, Integer, String, DateTime, Boolean


class AdminUserDO(Base):
    """
    后台管理用户
    """

    __tablename__ = "pm_admin_user"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(String(32), nullable=False, doc="用户ID")
    username = Column(String(64), nullable=False, doc="用户名称")
    password = Column(String(64), nullable=False, doc="用户密码")
    telephone = Column(String(15), nullable=False, doc="联系方式")
    email = Column(String(32), nullable=False, doc="邮箱")
    is_admin = Column(Integer, nullable=False, default=0, doc="是否管理员")  #0.否；1.是

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