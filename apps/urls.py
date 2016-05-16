#coding=utf-8
__author__ = 'wan'

from wx_app.wx_handler import WxIndexHandler



apps_handlers = [

    #********微信app URL********#
    (r'/access', WxIndexHandler)  #微信接入
]