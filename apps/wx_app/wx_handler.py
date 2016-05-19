#coding=utf-8
__author__ = 'wan'


from common.handlers.app_base_handler import AppBaseHandler
from common.wx_sdk.config import WX_TOKEN
from common.wx_sdk.base import WXChatBase

import logging
import traceback
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
        :return:
        """
        data = self.request.body
        wx_chat = WXChatBase()

        #ps.1.解析xml数据
        wx_chat.parse_data(data)

        #ps.2.根据解析出来的message进行逻辑处理
        message = wx_chat.message
        log.info(u"***********接收到的消息数据:{0}***********".format(message.convert_to_json()))

        #ps.3.返回消息
        resp = wx_chat.get_access_index()
        log.info(u"***********返回的消息数据:{0}***********".format(resp))

        return self.write(resp)


