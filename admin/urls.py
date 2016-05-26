#coding=utf-8
__author__ = 'wan'

from .wx_admin.handler import (WXConfigIndexHandler, WXMenuEditHandler, WXMenuListHandler, WXMenuParentListHandler, WXMenuDeleteHandler,
                               WXCreateMenuHandler)
from .user_admin.user_handler import (IndexHandler, AdminLoginHandler, AdminUserRegisterHandler, AdminLogoutHandler)

admin_handlers = [
    (r'/', IndexHandler),
    (r'/login', AdminLoginHandler),
    (r'/logout', AdminLogoutHandler),
    (r'/register', AdminUserRegisterHandler),

    ################微信相关##################
    (r'/admin/wx/config/list', WXConfigIndexHandler),   #微信配置列表
    (r'/admin/wx/menu/list', WXMenuListHandler),    #微信所有菜单列表
    (r'/admin/wx/parent/menu/list', WXMenuParentListHandler),   #微信一级菜单列表
    (r'/admin/wx/menu/editor', WXMenuEditHandler),  #微信菜单编辑
    (r'/admin/wx/menu/delete', WXMenuDeleteHandler),  #微信菜单删除

    (r'/app/wx/menu/create', WXCreateMenuHandler),  #微信公众号创建菜单
]