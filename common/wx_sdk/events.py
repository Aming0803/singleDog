#coding=utf-8
__author__ = 'wan'

import json
EVENT_TYPES = {}


def event_type(type):
    """
    事件类型
    :param type:
    :return:
    """
    def register(cls):
        EVENT_TYPES[type] = cls
        return cls
    return register


class WXEventBase(object):

    def __init__(self, message):
        """
        :param message:事件消息
        :return:
        """
        self.target = message.pop("ToUserName", "")
        self.source = message.pop("FromUserName", "")
        self.time = int(message.pop("CreateTime", 0))
        self.type = message.pop("MsgType", "event")
        self.event = message.pop("Event", "").lower()
        self.__dict__.update(message)

    def convert_to_json(self):
        """
        转化成json数据
        :return:
        """
        return json.dumps(self.__dict__)


@event_type("subscribe")
class WXSubscribeEvent(WXEventBase):

    def __init__(self, message):
        """
        关注事件
        :param message:
        :return:
        """
        super(WXSubscribeEvent, self).__init__(message)


@event_type("unsubscribe")
class WXUnSubscribeEvent(WXEventBase):

    def __init__(self, message):
        """
        取消关注事件
        :param message:
        :return:
        """
        super(WXUnSubscribeEvent, self).__init__(message)


@event_type("subscribe_scan")
class WXSubscribeScanEvent(WXEventBase):

    def __init__(self, message):
        """
        扫描二维码订阅,用户未关注时的事件推送
        :param message:
        :return:
        """
        self.key = message.pop("EventKey", "")
        self.ticket = message.pop("Ticket", "")
        super(WXSubscribeScanEvent, self).__init__(message)


@event_type("scan")
class WXScanEvent(WXEventBase):

    def __init__(self, message):
        """
        扫描二维码订阅,用户已关注时的事件推送
        :param message:
        :return:
        """
        self.key = message.pop("EventKey", "")
        self.ticket = message.pop("Ticket", "")
        super(WXScanEvent, self).__init__(message)


@event_type("location")
class WXLocationEvent(WXEventBase):

    def __init__(self, message):
        """
        上报地理位置
        用户同意上报地理位置后，每次进入公众号会话时，都会在进入时上报地理位置，或在进入会话后每5秒上报一次地理位置
        :param message:
        :return:
        """
        self.latitude = float(message.pop("Latitude", "0"))
        self.longitude = float(message.pop("Longitude", "0"))
        self.precision = float(message.pop("Precision", "0"))
        super(WXLocationEvent, self).__init__(message)


@event_type("click")
class WXClickEvent(WXEventBase):

    def __init__(self, message):
        """
        自定义菜单事件
        点击菜单拉取消息时的事件推送
        :param message:
        :return:
        """
        self.key = message.pop("EventKey", "")
        super(WXClickEvent, self).__init__(message)


@event_type("view")
class WXViewEvent(WXEventBase):

    def __init__(self, message):
        """
        自定义菜单事件
        点击菜单跳转链接时的事件推送
        :param message:
        :return:
        """
        self.key = message.pop("EventKey", "")
        super(WXViewEvent, self).__init__(message)


@event_type("masssendjobfinish")
class WXMessageSendALLEvent(WXEventBase):

    def __init__(self, message):
        """
        群发任务结束回调事件
        :param message:
        :return:
        """
        self.msg_id = message.pop("MsgID", "")
        self.status = message.pop("Status", "")
        self.total_count = int(message.pop("TotalCount", 0))
        self.filter_count = int(message.pop("FilterCount", 0))
        self.send_count = int(message.pop("SentCount", 0))
        self.error_count = int(message.pop("ErrorCount", 0))
        super(WXMessageSendALLEvent, self).__init__(message)










