#coding=utf-8
__author__ = 'wan'

"""
方法集合
"""

from .interfaces import (
    WXUserInfoApi, WXCustomMenuApi, WXUploadImageApi, WXTempMediaUploadApi, WXAddMaterialApi, WXUploadNewsApi, WXMessageSendAllByTagApi,
    WXSendMessageAllByOpenidApi
)
from services.wx_service import (
    WXUserService, WXMenuService, WXArticleService, WXMessageRecordService
 )

import os
import logging
log = logging.getLogger(__file__)

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
    log.info(u"**************用户openid:%s***********" % openid)
    #ps.请求用户信息接口
    wx_user_api = WXUserInfoApi()
    success, data = wx_user_api.make_request(openid)
    if not success:
        return False, data

    log.info(u"***********微信请求用户信息:%s*********" % data)
    #ps.判断该用户是否已保存, 已存在则更新订阅时间
    wx_user_ser = WXUserService()
    success, msg = wx_user_ser.handle_user_by_subscribe_event(openid, data)
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


def update_send_all_message(message):
    """
    反馈群发消息的处理
    :param message:
    :return:
    """
    if not message:
        return False, "数据不存在"

    wx_message_record_ser = WXMessageRecordService()
    msg_id = message.msg_id
    status = message.status
    total_count = message.total_count
    filter_count = message.filter_count
    send_count = message.send_count
    error_count = message.error_count

    success, msg = wx_message_record_ser.update_wx_message_record_by_msg_id(msg_id, status=status, total_count=total_count,
                                        filter_count=filter_count, send_count=send_count, error_count=error_count)
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
        if not child_menu_list:
            data = create_button(menu)
            menu_info['button'].append(data)
        else:
            info = {"name": menu.name}
            sub_menu = []
            for child_menu in child_menu_list:
                data = create_button(child_menu)
                # data["sub_button"] = []
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


def upload_the_image_method(file_path):
    """
    上传图文消息内的图片获取URL
    :param file_path:文件保存后的路径
    :return:
    """
    if not file_path or not os.path.exists(file_path):
        return False, "文件不存在"

    img_upload_api = WXUploadImageApi()
    data = {"media": open(file_path)}
    success, url = img_upload_api.make_request(data)
    return success, url


def wx_add_temp_media_method(media_type, file_path):
    """
    添加临时素材
    :param file_path:文件路径
    :param media_type:文件类型
    :return:字典
    """
    if not file_path or not os.path.exists(file_path):
        return False, "文件不存在"

    wx_temp_media_api = WXTempMediaUploadApi()
    data = {"media": open(file_path)}
    success, content = wx_temp_media_api.make_request(media_type, data)
    return success, content


def wx_add_permanent_other_media_method(media_type, file_path, **kwargs):
    """
    添加永久其他素材，图片，音频等
    :param media_type:
    :param file_path:
    :param kwargs:视频
    :return:
    """
    if not file_path or not os.path.exists(file_path):
        return False, "文件不存在"

    wx_per_other_media_api = WXAddMaterialApi()
    data = {"media": open(file_path)}

    for key, val in kwargs.iteritems():
        if val and isinstance(val, unicode):
            kwargs[key] = val.encode("utf-8")

    success, content = wx_per_other_media_api.make_request(media_type, data, **kwargs)
    return success, content


def wx_upload_message_news_method(article_id_list):
    """
    群发消息上传图文
    :param article_id_list:后台填写的文章id列表
    :return:
    """
    if not article_id_list or not isinstance(article_id_list, list):
        return False, "数据或格式不正确"

    #todo:上传图文素材
    wx_article_ser = WXArticleService()
    data = {"articles": []}
    excludes = ['gmt_created', 'gmt_modified', 'deleted', "id"]
    for article_id in article_id_list:
        article_id = int(article_id)
        article = wx_article_ser.get_article_by_article_id(article_id)
        article_info = article.convert_to_dict(excludes)
        data["articles"].append(article_info)

    wx_upload_news_api = WXUploadNewsApi()
    success, content = wx_upload_news_api.make_request(data)
    return success, content


def wx_send_all_news_by_tag(media_id):
    """
    群发图文
    :param media_id:
    :return:
    """
    if not media_id:
        return False, "media_id数据不存在"

    #ps.群发图文数据格式
    data = {
        "filter":{
            "is_to_all": True
        },
        "mpnews":{
            "media_id": media_id
        },
        "msgtype": "mpnews"
    }

    wx_send_message_api = WXMessageSendAllByTagApi()
    success, content = wx_send_message_api.make_request(data)
    log.info(u"************群发返回内容:{0}*********".format(content))

    return success, content


def wx_send_all_news_by_openid(media_id, open_id_list=None):
    """
    群发图文
    :param media_id:
    :return:
    """
    if not media_id:
        return False, "media_id数据不存在"

    if not open_id_list:
        wx_user_ser = WXUserService()
        user_list = wx_user_ser.get_all_subscribe_user_list()
        open_id_list = [u.openid for u in user_list]

    #ps.群发图文数据格式
    data = {
        "to_user": open_id_list,
        "mpnews":{
            "media_id": media_id
        },
        "msgtype": "mpnews"
    }

    wx_send_message_api = WXSendMessageAllByOpenidApi()
    success, content = wx_send_message_api.make_request(data)
    log.info(u"************群发返回内容:{0}*********".format(content))

    return success, content








if __name__ == '__main__':
    success, msg = wx_send_all_news_by_tag("5zBVzpqy7-UgHaWadwDBWbBoY8GCPdphXb5LUi24RDf8jjXDPcQDhuCUyLz1m1Qs")
    print success, msg