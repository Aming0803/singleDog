#coding=utf-8
__author__ = 'wan'

from services.wx_service import WXMenuService

MENU_TYPE = {
    "click": "点击推事件",
    "view": "跳转URL",
    "media_id": "发送消息(除文本)",
    "view_limited": "跳转图文消息URL"
}

REPLY_TYPE = {
    "text": "文本",
    "image": "图片",
    "voice": "语音",
    "video": "视频",
    "music": "音乐",
    "news": "图文",
}

MEDIA_TYPE = {
    "image": "图片",
    "voice": "语音",
    "video": "视频",
    "thumb": "缩略图"
}

MEDIA_ALL_TYPE = {
    "image": "图片",
    "voice": "语音",
    "video": "视频",
    "thumb": "缩略图",
    "news": "图文",
}


def get_menu_name_by_category(category):
    """
    获取菜单的名称
    :param category:
    :return:
    """
    if not category:
        return ""

    category = int(category)

    if category == 1:
        return "一级菜单"

    elif category == 2:
        return "二级菜单"
    else:
        return category

def get_parent_menu_name(parent_id):
    """
    获取父菜单的名称
    :param parent_id:
    :return:
    """
    if not parent_id:
        return ""

    menu_ser = WXMenuService()
    menu = menu_ser.get_menu_by_id(parent_id)
    name = menu.name if menu else ""

    return name

def get_menu_type_name(menu_type):
    """
    根据类型获取名称
    :param menu_type:
    :return:
    """

    if not menu_type:
        return ""

    if MENU_TYPE.has_key(menu_type):
        return MENU_TYPE[menu_type]
    else:
        return ""

def get_reply_type_name(reply_type):
    """
    获取回复类型名称
    :param reply_type:
    :return:
    """
    if not reply_type or not REPLY_TYPE.has_key(reply_type):
        return ""

    return REPLY_TYPE[reply_type]

def get_content_display_length(content, length=15):
    """
    获取一定的长度显示
    :param content:
    :param length:
    :return:
    """
    if not content:
        return ""

    new_content = content[0: length]
    return u"{0}...".format(new_content)

def get_media_category_name(category):
    """
    获取素材类别
    :param category:
    :return:
    """
    if not category:
        return ""

    category = int(category)
    if category == 1:
        return "临时素材"

    elif category == 2:
        return "永久素材"

    elif category == 3:
        return "群发素材"
    else:
        return ""

def get_media_type(media_type):
    """
    获取素材类型
    :param media_type:
    :return:
    """
    if not media_type:
        return ""

    if not MEDIA_ALL_TYPE.has_key(media_type):
        return media_type

    return MEDIA_ALL_TYPE[media_type]
