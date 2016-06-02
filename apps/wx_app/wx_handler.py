#coding=utf-8
__author__ = 'wan'


from common.handlers.app_base_handler import AppBaseHandler
from common.wx_sdk.config import WX_TOKEN
from common.wx_sdk.base import WXChatBase
from common.wx_sdk.methods import (
    update_wx_user_location_info, update_send_all_message
)
from taskCelery.tasks import create_wx_user
from services.wx_service import WXReplyService

import logging
log = logging.getLogger(__file__)


class WxIndexHandler(AppBaseHandler):

    def get(self):
        """
        验证公众号
        :return:
        """
        signature = self.get_argument("signature", "")
        timestamp = self.get_argument("timestamp", "")
        nonce = self.get_argument("nonce", "")
        echostr = self.get_argument("echostr", "")

        if not signature or not timestamp or not nonce or not echostr:
            return self.write("无效请求")

        #todo:验证签名
        wx_chat = WXChatBase()
        sign = wx_chat.get_access_sign(token=WX_TOKEN, timestamp=timestamp, nonce=nonce)

        if sign == signature:
            return self.write(echostr)
        else:
            return self.write("无效请求")

    def post(self):
        """
        进行相关操作
        先关注再上传地理信息位置
        :return:
        """
        data = self.request.body
        wx_chat = WXChatBase()

        #ps.1.解析xml数据
        wx_chat.parse_data(data)

        #ps.2.根据解析出来的message进行逻辑处理
        message = wx_chat.message
        log.info(u"***********接收到的消息数据:{0}***********".format(message.convert_to_json()))

        #ps.3.业务逻辑处理
        message_type = message.type
        if message_type == "event":
            resp = self.handler_the_event_message(wx_chat)
        else:
            resp = self.handler_the_common_message(wx_chat)

        log.info(u"***********返回的消息数据:{0}***********".format(resp))
        return self.write(resp)

    def handler_the_event_message(self, wx_chat):
        """
        处理事件消息
        :param wx_chat: WxChatBase类
        :return:
        """
        message = wx_chat.message
        event = message.event
        openid = message.source

        resp = ""
        #todo:用户订阅或者取消订阅时候, 用户操作
        if event == "subscribe":
            create_wx_user.apply_async((openid))
            resp = wx_chat.get_access_index()

        if event == "unsubscribe":
            create_wx_user.apply_async((openid))

        #todo:用户地理位置信息
        if event == "location":
            latitude = message.latitude
            longitude = message.longitude
            success, msg = update_wx_user_location_info(openid, latitude=latitude, longitude=longitude)
            log.info(u"*************更新用户地理位置结果:{0}|{1}*******".format(success, msg))

        #todo:菜单点击事件
        if event == "click":
            key = message.key
            wx_reply_ser = WXReplyService()
            wx_reply = wx_reply_ser.get_reply_by_key(key)
            if wx_reply:
                content = wx_reply.content
                resp = wx_chat.response_text(content)
            else:
                resp = wx_chat.get_access_index()

        #todo:群发消息回调,保存群发消息反馈结果
        if event == 'messsendjobfinish':
            success, msg = update_send_all_message(wx_chat.message)
            log.info(u"*************群发消息回调处理结果:{0}|{1}*******".format(success, msg))

        return resp

    def handler_the_common_message(self, wx_chat):
        """
        处理普通消息
        暂时处理下文本和图片信息
        :param wx_chat: WxChatBase类
        :return:
        """
        message_type = wx_chat.message.type

        if message_type == 'text':
            key = wx_chat.message.content
            wx_reply_ser = WXReplyService()
            wx_reply = wx_reply_ser.get_reply_by_key(key)
            if wx_reply:
                content = wx_reply.content
                resp = wx_chat.response_text(content)
            else:
                resp = wx_chat.get_access_index()

        elif message_type == 'image':
            media_id = "wR1EfcKZlL9Xz96T-AEbov5bCjIYN0GNjMd3ceYq-0g"
            resp = wx_chat.response_image(media_id)

        else:
            resp = wx_chat.get_access_index()

        return resp