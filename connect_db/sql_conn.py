#coding=utf-8
__author__ = 'wan'

from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import *



# DB_URL = URL(DB_DRIVE_NAME, username=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, database=DB_NAME, query=DB_QUERY)
engine = create_engine(DB_URL, echo=db_echo, pool_size=db_pool_size, max_overflow=db_max_overflow, pool_recycle=db_pool_recycle, isolation_level="READ UNCOMMITTED")
session_factory = scoped_session(sessionmaker(bind=engine, autoflush=db_autoflush, autocommit=db_autocommit))
db_session = session_factory()



class MyDBConnect(object):
    @property
    def mysql_conn(self):
        if not hasattr(self, "_db"):
            self._db = db_session
        return self._db


SQL_DB = MyDBConnect().mysql_conn
