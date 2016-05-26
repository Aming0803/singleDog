#coding=utf-8
__author__ = 'wan'

"""
方法集合
"""

from .interfaces import WXUserInfoApi, WXCustomMenuApi
from services.wx_service import WXUserService, WXMenuService

MENU_TYPE_KEY = {
    "click": "key",
    "view": "url",
    "scancode_waitmsg": "rselfmenu_0_0",
    "scancode_push": "rselfmenu_0_1",
    "pic_sysphoto": "rselfmenu_1_0",
    "pic_photo_or_album": "rselfmenu_1_1",
    "pic_weixin": "rselfmenu_1_2",
    "location_select": "rselfmenu_2_0",
    "media_id": "MEDIA_ID1",
    "view_limited": "MEDIA_ID2",
}



def create_wx_user_by_openid_method(openid):
    """
    用户在关注等之后保存用户信息
    :param openid:
    :return:
    """
    #ps.判断该用户是否已保存
    wx_user_ser = WXUserService()
    wx_user = wx_user_ser.get_user_by_openid(openid)
    if wx_user:
        return False, "该用户已存在"

    #ps.2.请求用户信息接口
    wx_user_api = WXUserInfoApi()
    success, data = wx_user_api.make_request(openid)
    if not success:
        return False, data

    #ps.3.根据返回数据保存用户
    success, msg = wx_user_ser.create_user_by_resp_data(data)
    return success, msg


def update_wx_user_location_info(openid, **kwargs):
    """
    更改用户的地理位置信息
    :param openid:
    :param kwargs:
    :return:
    """
    wx_user_ser = WXUserService()
    success, msg = wx_user_ser.update_wx_info_by_openid(openid, **kwargs)
    return success, msg


def create_custom_menu_method():
    """
    创建菜单
    根据menu表生成数据
    自定义菜单最多包括3个一级菜单，每个一级菜单最多包含5个二级菜单
    :return:
    """
    #ps.生成菜单数据
    wx_menu_ser = WXMenuService()
    active_parent_menu_list = wx_menu_ser.get_active_parent_menu_list()
    if not active_parent_menu_list:
        return False, "无使用的菜单数据"

    menu_info = {"button":[]}
    parent_menu_list = active_parent_menu_list[0:3]
    for menu in parent_menu_list:
        menu_id = menu.id
        child_menu_list = wx_menu_ser.get_active_child_menu_list(menu_id)[0:5]

        #length=1表示没有子菜单
        if len(child_menu_list) <= 1:
            data = create_button(menu)
            menu_info['button'].append(data)
        else:
            info = {"name": menu.name}
            sub_menu = []
            for child_menu in child_menu_list:
                if child_menu.id == menu_id:
                    continue
                data = create_button(child_menu)
                data["sub_button"] = []
                sub_menu.append(data)
            info["sub_button"] = sub_menu
            menu_info["button"].append(info)

    wx_menu_api = WXCustomMenuApi()
    code, msg = wx_menu_api.make_request(menu_info)
    if code == 0:
        success = True
        msg = "创建成功"
    else:
        success = False

    return success, msg


def create_button(menu):
    """
    根据menu生成button
    :param menu:
    :return:
    """
    data = {"name": menu.name}
    menu_type = menu.menu_type
    field = MENU_TYPE_KEY.get(menu_type)
    value = menu.value
    data["type"] = menu_type
    data[field] = value
    return data
