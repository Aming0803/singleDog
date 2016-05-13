#coding=utf-8
__author__ = 'wan'


####RDBMS CONFIG#####
DB_DRIVE_NAME = "mysqldb"
DB_USERNAME = "root"
DB_PASSWORD = "ysletmein"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "wxurban"
DB_QUERY = {"charset": "utf8"}

DB_URL = "mysql://root:ysletmein@127.0.0.1:3306/wxurban?charset=utf8"



db_pool_size = 30
db_max_overflow = 30
db_echo=False
db_pool_size=30
db_max_overflow=70
db_pool_recycle=5
db_autoflush=False
db_autocommit=False









##############################
#redis setting
redis_server_env = '127.0.0.1'
redis_server_port = 6379
redis_server_passwd = 'wmmishandsomeman123456'


##############################
#mongodb
mongodb_server_ip = '127.0.0.1'
mongodb_server_port = 27017         #default

##use name pwd
mongodb_url = "mongodb://wan:wan@localhost:27017/"