#coding=utf-8
__author__ = 'wan'

import requests
import json
import logging
import traceback

from config import TEST_WX_APP_ID, TEST_WX_APP_SECRET
from connect_db.redis_conn import REDIS_DB
from common.config import WX_KEY, WX_ACCESS_TOKEN
from .utils import CharsetConvert

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


class WXBaseApi(object):

    def __init__(self):
        """
        父类
        :return:
        """
        self.redis = REDIS_DB

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


class WXCustomMenuApi(WXBaseApi):

    _request_url = "https://api.weixin.qq.com/cgi-bin/menu/create"
    _request_method = "POST"

    def __init__(self):
        """
        自定义菜单
        :return:
        """
        super(WXCustomMenuApi, self).__init__()

    def make_request(self, params):
        """
        :param params:
        :return:
        """

        log.info(u"************菜单数据:{0}**************".format(params))

        if not isinstance(params, dict):
            return False, "参数格式不正确"

        success, access_token = self.get_access_token()
        if not success:
            return False, access_token

        #ps.注意了,这个地方比较奇葩,首先,需要将unicode转化为utf-8字符,同时json化,注意ensure_ascii=False不然会产生unicode，最后post的竟然是json字符串
        chart_convert_tool = CharsetConvert()
        data = json.dumps(chart_convert_tool._transcoding_dict(params), ensure_ascii=False)

        request_url = "{0}?access_token={1}".format(self._request_url, access_token)
        req = requests.post(request_url, data=data)
        resp = req.content

        content = json.loads(resp)
        errcode, msg = content["errcode"], content["errmsg"]
        log.info(u"***************设置自定义菜单结果:{0}|{1}*******************".format(errcode, msg))

        return errcode, msg


class WXMenuDeleteApi(WXBaseApi):

    _request_url = "https://api.weixin.qq.com/cgi-bin/menu/delete"
    _request_method = "GET"

    def __init__(self):
        """
        删除当前菜单
        :return:
        """
        super(WXMenuDeleteApi, self).__init__()

    def make_request(self):
        """
        :return:
        """
        success, access_token = self.get_access_token()
        if not success:
            return False, access_token

        request_url = "{0}?access_token={1}".format(self._request_url, access_token)
        req = requests.get(request_url)
        resp = req.content

        content = json.loads(resp)
        if content.has_key("errcode"):
            errmsg = content["errmsg"]
            log.info(u"*************删除菜单接口,原因:%s***********" % errmsg)
            return False, errmsg
        else:
            return True, content


class WXUserInfoApi(WXBaseApi):

    _request_url = "https://api.weixin.qq.com/cgi-bin/user/info"
    _request_method = "GET"

    _lang = "zh_CN"

    def __init__(self):
        """
        获取用户信息
        :return:
        """
        super(WXUserInfoApi, self).__init__()

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


class WXUploadImageApi(WXBaseApi):

    _request_url = "https://api.weixin.qq.com/cgi-bin/media/uploadimg"
    _request_method = "POST"

    def __init__(self):
        """
        微信上传图文消息内的图片获取URL
        :return:
        """
        super(WXUploadImageApi, self).__init__()

    def make_request(self, media):
        """
        :param media:form-data中媒体文件标识，有filename、filelength、content-type等信息，file对象
        :return:
        """
        success, access_token = self.get_access_token()
        if not success:
            return False, access_token

        request_url = "{0}?access_token={1}".format(self._request_url, access_token)
        req = requests.post(request_url, files=media)
        resp = req.content

        content = json.loads(resp)
        if content.has_key("url"):
            log.info("*************微信上传图文消息内的图片获取URL接口成功***********")
            return True, content['url']
        else:
            code, msg = content["errcode"], content["errmsg"]
            log.info(u"*************微信上传图文消息内的图片获取URL接口失败,原因:%s|%s***********" % (code, msg))
            return False, msg


class WXTempMediaUploadApi(WXBaseApi):

    #https://api.weixin.qq.com/cgi-bin/media/upload?access_token=ACCESS_TOKEN&type=TYPE
    _request_url = "https://api.weixin.qq.com/cgi-bin/media/upload"
    _request_method = "POST"

    def __init__(self):
        """
        新增临时素材
        :return:
        """
        super(WXTempMediaUploadApi, self).__init__()

    def make_request(self, media_type, media):
        """
        ps:注意 缩略图返回的数据不含media_id是thumb_media_id
        :param 分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        :param media:form-data中媒体文件标识，有filename、filelength、content-type等信息，file对象
        :return:
        """
        success, access_token = self.get_access_token()
        if not success:
            return False, access_token

        request_url = "{0}?access_token={1}&type={2}".format(self._request_url, access_token, media_type)
        req = requests.post(request_url, files=media)
        resp = req.content

        content = json.loads(resp)
        if content.has_key("media_id") or content.has_key("thumb_media_id"):
            log.info("*************新增临时素材接口成功***********")
            return True, content
        else:
            code, msg = content["errcode"], content["errmsg"]
            log.info(u"*************新增临时素材接口失败,原因:%s|%s***********" % (code, msg))
            return False, msg


class WXAddMaterialApi(WXBaseApi):

    #https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=ACCESS_TOKEN&type=TYPE
    _request_url = "https://api.weixin.qq.com/cgi-bin/material/add_material"
    _request_method = "POST"

    def __init__(self):
        """
        新增其他类型永久素材,不包括图文
        通过POST表单来调用接口，表单id为media，包含需要上传的素材内容，有filename、filelength、content-type等信息
        :return:
        """
        super(WXAddMaterialApi, self).__init__()

    def make_request(self, media_type, media, **kwargs):
        """
        :param media_type: 素材类型：媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        :param media:form-data中媒体文件标识，有filename、filelength、content-type等信息
        :param kwargs:针对视频，在上传视频素材时需要POST另一个表单，id为description，包含素材的描述信息，title/introduction
        :return:
        """
        success, access_token = self.get_access_token()
        if not success:
            return False, access_token

        request_url = "{0}?access_token={1}&type={2}".format(self._request_url, access_token, media_type)
        if media_type == "video":
            title = kwargs.get("title")
            introduction = kwargs.get("introduction")
            description = {"title":title, "introduction": introduction}
            data = json.dumps(description, ensure_ascii=False)
            req = requests.post(request_url, files=media, data=data)
        else:
            req = requests.post(request_url, files=media)
        resp = req.content

        content = json.loads(resp)
        if content.has_key("media_id"):
            log.info("*************新增临时素材接口成功***********")
            return True, content
        else:
            code, msg = content["errcode"], content["errmsg"]
            log.info(u"*************新增临时素材接口失败,原因:%s|%s***********" % (code, msg))
            return False, msg


class WXAddNewsApi(WXBaseApi):

    _request_url = "https://api.weixin.qq.com/cgi-bin/material/add_news"
    _request_method = "POST"

    def __init__(self):
        """
        新增永久图文素材
        用于菜单
        :return:
        """
        super(WXAddNewsApi, self).__init__()

    def make_request(self, article):
        """
        :param articles: 字典
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1444738729&token=&lang=zh_CN
        :return:
        """
        success, access_token = self.get_access_token()
        if not success:
            return False, access_token

        request_url = "{0}?access_token={1}".format(self._request_url, access_token)
        req = requests.post(request_url, data=article)
        resp = req.content

        content = json.loads(resp)
        if content.has_key("media_id"):
            log.info("*************新增永久图文素材接口成功***********")
            return True, content['url']
        else:
            code, msg = content["errcode"], content["errmsg"]
            log.info(u"*************新增永久图文素材接口失败,原因:%s|%s***********" % (code, msg))
            return False, msg


class WXUploadNewsApi(WXBaseApi):

    _request_url = "https://api.weixin.qq.com/cgi-bin/media/uploadnews"
    _request_method = "POST"

    def __init__(self):
        """
        群发接口
        上传图文消息素材
        注意:群发上传图文素材种的thumb_media_id是临时素材，不能用永久素材
        :return:
        """
        super(WXUploadNewsApi, self).__init__()

    def make_request(self, article):
        """
        :param articles: 字典
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140549&token=&lang=zh_CN
        :return:
        """
        success, access_token = self.get_access_token()
        if not success:
            return False, access_token

        chart_convert_tool = CharsetConvert()
        data = json.dumps(chart_convert_tool._transcoding_dict(article), ensure_ascii=False)

        request_url = "{0}?access_token={1}".format(self._request_url, access_token)
        req = requests.post(request_url, data=data)
        resp = req.content

        content = json.loads(resp)
        if content.has_key("media_id"):
            log.info("*************群发之上传图文消息素材接口成功***********")
            return True, content
        else:
            code, msg = content["errcode"], content["errmsg"]
            log.info(u"*************群发之上传图文消息素材接口失败,原因:%s|%s***********" % (code, msg))
            return False, msg


class WXMessageSendAllByTagApi(WXBaseApi):
    """
    根据标签进行群发
    """
    _request_url = "https://api.weixin.qq.com/cgi-bin/message/mass/sendall"
    _request_method = "POST"

    def __init__(self):
        """
        根据标签进行群发
        :return:
        """
        super(WXMessageSendAllByTagApi, self).__init__()

    def make_request(self, message):
        """
        群发
        :param message:消息类型,图文,文本,视频等格式均不相同
        :return:
        """
        success, access_token = self.get_access_token()
        if not success:
            return False, access_token

        chart_convert_tool = CharsetConvert()
        data = json.dumps(chart_convert_tool._transcoding_dict(message), ensure_ascii=False)
        request_url = "{0}?access_token={1}".format(self._request_url, access_token)
        req = requests.post(request_url, data=data)
        resp = req.content

        content = json.loads(resp)
        if content.has_key("msg_id"):
            log.info("*************根据标签分组群发接口成功***********")
            return True, content
        else:
            code, msg = content["errcode"], content["errmsg"]
            log.info(u"*************根据标签分组群发接口失败,原因:%s|%s***********" % (code, msg))
            return False, msg


class WXSendMessageAllByOpenidApi(WXBaseApi):
    """
    根据openid进行群发
    """
    _request_url = "https://api.weixin.qq.com/cgi-bin/message/mass/send"
    _request_method = "POST"

    def __init__(self):
        """
        根据openid群发
        :return:
        """
        super(WXSendMessageAllByOpenidApi, self).__init__()

    def make_request(self, message):
        """
        群发
        :param message:消息类型,图文,文本,视频等格式均不相同
        :return:
        """
        success, access_token = self.get_access_token()
        if not success:
            return False, access_token

        chart_convert_tool = CharsetConvert()
        data = json.dumps(chart_convert_tool._transcoding_dict(message), ensure_ascii=False)
        request_url = "{0}?access_token={1}".format(self._request_url, access_token)
        req = requests.post(request_url, data=data)
        resp = req.content

        content = json.loads(resp)
        if content.has_key("msg_id"):
            log.info("*************根据OPENID群发接口成功***********")
            return True, content
        else:
            code, msg = content["errcode"], content["errmsg"]
            log.info(u"*************根据OPENID群发接口失败,原因:%s|%s***********" % (code, msg))
            return False, msg