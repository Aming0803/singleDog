#coding=utf-8
__author__ = 'wan'

import six
import time

from .messages import MESSAGE_TYPES, UnknownMessage
from .events import EVENT_TYPES
from .replies import (
    TextReply, ImageReply, MusicReply, VideoReply, VoiceReply, Article, ArticleReply
)
from .parser import XMLStore
from .utils import to_text, to_binary
from .config import WX_ACCESS_INDEX
from common.utils.pwd_util import create_sha1



class WXChatBase(object):

    def __init__(self):
        """
        微信功能基础类
        :return:
        """
        self._message = None
        self._has_parser = False

    def get_access_sign(self, **kwargs):
        """
        微信接入验证
        :param kwargs:
        token: 令牌
        timestamp:时间戳
        nonce:随即数
        :return:
        """
        sign_str = "".join(sorted(kwargs.values()))
        sign = create_sha1(sign_str)
        return sign

    @property
    def is_parser(self):
        """
        是否已经解析数据
        :return:
        """
        return self._has_parser

    def parse_data(self, xml_string):
        """
        解析接收到到xml数据
        :param xml_string:
        :return:
        """
        if isinstance(xml_string, six.text_type):
            xml_string = xml_string.encode('utf-8')

        xml_obj = XMLStore(xml_string)
        result = xml_obj.xml2dict
        msg_type = result["MsgType"].lower()

        #ps.普通消息类型和事件类型消息区分
        if msg_type == "event":
            event = result["Event"].lower()
            if event == "subscribe" and result.has_key("EventKey"):
                event_class = EVENT_TYPES["subscribe_scan"]
            else:
                event_class = EVENT_TYPES[event]

            self._message = event_class[result]

        else:
            message_class = MESSAGE_TYPES[msg_type]
            self._message = message_class(result)

        self._has_parser = True

    @property
    def message(self):
        """
        获取message转化未dict的信息
        :return:
        """
        return self.get_message()

    def get_message(self):
        """
        获取message转化未dict的信息
        :return:
        """
        return self._message

    def response_text(self, content):
        """
        文本消息回复
        :param content:
        :return:
        """
        return TextReply(self._message, content).render()

    def response_image(self, media_id):
        """
        图片消息回复
        :param media_id:通过素材管理中的接口上传多媒体文件，得到的id。
        :return:
        """
        return ImageReply(self._message, media_id).render()

    def response_voice(self, media_id):
        """
        回复语音
        :param media_id:通过素材管理中的接口上传多媒体文件，得到的id
        :return:
        """
        return VoiceReply(self._message, media_id).render()

    def response_video(self, media_id, title="", description=""):
        """
        回复视频
        :param media_id:
        :return:
        """
        return VideoReply(self._message, media_id, title=title, description=description).render()

    def response_music(self, music_url, title=None, description=None, hq_music_url=None, thumb_media_id=None):
        """
        回复音乐
        :param music_url:
        :param title:
        :param description:
        :param hq_music_url:
        :param thumb_media_id:
        :return:
        """
        pass

    def response_news(self, articles):
        """
        回复图文消息
        :param articles:包含字典的列表
        :return:
        """
        news = ArticleReply(self._message)
        for article in articles:
            item = Article(**article)
            news.add_article(item)

        return news.render()

    def _escape_code_to_unicode(self, data, code="utf-8"):
        """
        转化字符to unicode
        :param code:
        :return:
        """
        if not isinstance(data, unicode) and hasattr(data, "decode"):
            return data.decode(code)

        return data

    def _escape_code_to_string(self, data, code="utf-8"):
        """
        转化字符to string
        :param data:
        :param code:
        :return:
        """
        if not isinstance(data, basestring) and hasattr(data, "encode"):
            return data.encode(code)

        return data

    def get_access_index(self):
        """
        进入首页信息
        :return:
        """
        return self.response_text(WX_ACCESS_INDEX)
