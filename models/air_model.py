#coding=utf-8
__author__ = 'wan'

from base_model import Base
from sqlalchemy.sql.functions import now
from sqlalchemy import Column, Integer, String, DateTime, Boolean


class AirInfoDO(Base):

    __tablename__ = 'pm_air_info'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    date = Column(String(32), nullable=False, doc="飞行日期")
    flight = Column(String(128), nullable=False, doc="航程")
    card = Column(String(32), nullable=False, doc="身份证")
    province = Column(Integer, nullable=False, doc="省份代码")
    city = Column(Integer, nullable=False, doc="城市代码")
    count = Column(Integer, nullable=False, doc="航段数")

    gmt_created = Column(DateTime, default=now())
    gmt_modified = Column(DateTime, default=now())
    deleted = Column(Boolean, nullable=False, default=0)