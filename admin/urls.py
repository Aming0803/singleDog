#coding=utf-8
__author__ = 'wan'

from .wx_admin.handler import (WXConfigIndexHandler, WXMenuEditHandler, WXMenuListHandler, WXMenuParentListHandler, WXMenuDeleteHandler,
    WXCreateMenuHandler, WXReplyListHandler, WXReplyEditorHandler, WXReplyDeleteHandler, WXImageUploadHandler, WXUploadImgListHandler,
    WXUploadImgDetailHandler, WXArticleListHandler, WXAddArticleHandler, WXAddTempMediaHandler, WXMediaListHandler,
    WXAddPermanentOtherMediaHandler, WXSendNewMessagesHandler
                               )
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

    (r'/admin/wx/reply/list', WXReplyListHandler),  #回复列表
    (r'/admin/wx/reply/editor', WXReplyEditorHandler),  #回复编辑
    (r'/admin/wx/reply/delete', WXReplyDeleteHandler),  #回复删除

    (r'/admin/wx/img/list', WXUploadImgListHandler),  #微信上传图文消息内的图片获取URL列表
    (r'/admin/wx/img/detail', WXUploadImgDetailHandler),  #微信上传图文消息内的图片获取URL详情

    (r'/admin/wx/article/list', WXArticleListHandler),  #图文文章列表
    (r'/admin/wx/article/detail', WXUploadImgDetailHandler),  #微信上传图文消息内的图片获取URL详情
    (r'/admin/wx/article/add', WXAddArticleHandler),  #添加图文文章

    (r'/admin/wx/media/list', WXMediaListHandler),  #素材列表
    (r'/admin/wx/temp/media/add', WXAddTempMediaHandler),  #微信临时素材的添加
    (r'/admin/wx/per/media/add', WXAddPermanentOtherMediaHandler),  #微信永久其他素材的添加

    (r'/admin/wx/news/message', WXSendNewMessagesHandler),  #群发图文消息
    (r'/admin/wx/other/message', WXAddPermanentOtherMediaHandler),  #微信永久其他素材的添加

    (r'/app/wx/menu/create', WXCreateMenuHandler),  #微信公众号创建菜单
    (r'/app/wx/img/upload', WXImageUploadHandler),  #微信上传图文消息内的图片获取URL上传
]