# coding=utf-8
__author__ = 'wan'

import os
import sys

current_path = os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(__file__))

from models.base_model import Base
from sqlalchemy import create_engine
from connect_db.config import DB_URL

from models.wx_model import WXMenuDO
# from models.wx_model import WXConfigDO, WXImageUploadDO, WXMediaDO
# from models.user_model import AdminUserDO







def main():
    engine = create_engine(DB_URL, encoding="utf-8", echo=True)
    Base.metadata.create_all(engine)










if __name__ == "__main__":
    main()