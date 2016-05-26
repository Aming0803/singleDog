#coding=utf-8
__author__ = 'wan'

import socket
local_ip = socket.gethostbyname(socket.gethostname())

##########微信redis存储
WX_KEY = "WX_CONFIG"
WX_ACCESS_TOKEN = "WX_ACCESS_TOKEN"



##########网站cookie保存域名#########
if local_ip == "10.252.91.123":
    DOMAIN = "http://wx.wefresh.me/"
else:
    DOMAIN = "localhost"