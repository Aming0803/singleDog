#coding=utf-8
__author__ = 'wan'


from common.handlers.app_base_handler import AppBaseHandler
from common.wx_sdk.config import WX_TOKEN
from common.utils.pwd_util import create_sha1


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
        sign_list = [WX_TOKEN, timestamp, nonce]
        sign_list.sort()
        sign_str = "".join(sign_list)
        sign = create_sha1(sign_str)

        if sign == signature:
            return self.write(echostr)
        else:
            return self.write("无效请求")

    def post(self):
        """
        进行相关操作
        :return:
        """