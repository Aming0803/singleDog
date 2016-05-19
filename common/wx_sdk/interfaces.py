#coding=utf-8
__author__ = 'wan'

import requests
import json
import logging
import traceback

from config import TEST_WX_APP_ID, TEST_WX_APP_SECRET
from connect_db.redis_conn import REDIS_DB
from common.config import WX_KEY, WX_ACCESS_TOKEN

log = logging.getLogger(__file__)


class WXAccessTokenApi(object):

    _request_url = "https://api.weixin.qq.com/cgi-bin/token"
    _request_method = "GET"

    def __init__(self):
        """
        获取access_token的api
        :return:
        """
        self.grant_type = "client_credential"
        self.appid = TEST_WX_APP_ID
        self.secret = TEST_WX_APP_SECRET

    def make_request(self):
        """
        :return:
        """
        redis_db = REDIS_DB

        req = requests.get(self._request_url, params=self.__dict__)
        resp = req.content
        content = json.loads(resp)

        if content.has_key("access_token"):
            access_token = content.get("access_token")
            redis_db.set(WX_ACCESS_TOKEN, access_token, ex=3600)
            log.info("*****************获取ACCESS_TOKEN成功****************")
            return access_token

        else:
            errmsg = content["errmsg"]
            log.info("*****************获取ACCESS_TOKEN失败****************")
            log.error(u"************失败原因:%s***********".format(errmsg))
            return ""


class WXCustomViewApi(object):

    #https://api.weixin.qq.com/cgi-bin/menu/create?access_token=ACCESS_TOKEN
    _request_url = "https://api.weixin.qq.com/cgi-bin/menu/create"
    _request_method = "POST"

    def __init__(self):
        """
        自定义菜单
        :return:
        """
        self.redis = REDIS_DB

    def make_request(self, params):
        """
        :param params:
        :return:
        """
        if not isinstance(params, dict):
            return False, "参数格式不正确"

        success, access_token = self.get_access_token()
        if not success:
            return False, access_token

        request_url = "{0}?access_token={1}".format(self._request_url, access_token)
        req = requests.post(request_url, data=params)
        resp = req.content

        content = json.loads(resp)
        errcode, msg = content["errcode"], content["errmsg"]
        log.info(u"***************设置自定义菜单结果:{0}|{1}*******************".format(errcode, msg))

        return errcode, msg

    def get_access_token(self):
        """
        获取微信access_token
        :return:
        """
        if self.redis.exists(WX_ACCESS_TOKEN):
            access_token = self.redis.get(WX_ACCESS_TOKEN)
        else:
            wx_access_token_api = WXAccessTokenApi()
            access_token = wx_access_token_api.make_request()
            if not access_token:
                log.info("************access_token不存在************")
                return False, "access_token不存在"

        return True, access_token


class WXUserInfoApi(object):

    _request_url = "https://api.weixin.qq.com/cgi-bin/user/info"
    _request_method = "GET"

    _lang = "zh_CN"

    def __init__(self):
        """
        获取用户信息
        :return:
        """
        self.redis = REDIS_DB

    def make_request(self, open_id):
        """
        :param open_id:用户OPEN_ID
        :return:
        """
        if not open_id:
            return False, "用户OPEN_ID不存在"

        success, access_token = self.get_access_token()
        if not success:
            return False, access_token

        params = {"access_token": access_token, "openid": open_id, "lang": self._lang}
        req = requests.get(self._request_url, params=params)
        resp = req.content

        content = json.loads(resp)
        if content.has_key("errcode"):
            errmsg = content["errmsg"]
            log.info(u"*************请求用户信息接口失败,原因:%s***********" % errmsg)
            return False, errmsg

        else:
            return True, content


    def get_access_token(self):
        """
        获取微信access_token
        :return:
        """
        if self.redis.exists(WX_ACCESS_TOKEN):
            access_token = self.redis.get(WX_ACCESS_TOKEN)
        else:
            wx_access_token_api = WXAccessTokenApi()
            access_token = wx_access_token_api.make_request()
            if not access_token:
                log.info("************access_token不存在************")
                return False, "access_token不存在"

        return True, access_token




