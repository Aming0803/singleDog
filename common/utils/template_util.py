#coding=utf-8
__author__ = 'wan'

from services.wx_service import WXMenuService

MENU_TYPE = {
    "click": "点击推事件",
    "view": "跳转URL",
    "media_id": "发送消息(除文本)",
    "view_limited": "跳转图文消息URL"
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