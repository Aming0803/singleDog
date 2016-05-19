#coding=utf-8
__author__ = 'wan'


MESSAGE_TYPES = {}


def message_type(type):
    """
    message_type
    :param type:
    :return:
    """

    def register(cls):
        MESSAGE_TYPES[type] = cls
        return cls
    return register


class WXAcceptMessageBase(object):

    def __init__(self, message):
        """
        :param message:
        :return:
        """
        self.msg_id = int(message.pop("MsgId", 0))
        self.target = message.pop("ToUserName", "")
        self.source = message.pop("FromUserName", "")
        self.time = int(message.pop("CreateTime", 0))
        self.type = message.pop("MsgType", "")
        self.__dict__.update(message)


@message_type("text")
class WXAccessTextMessage(WXAcceptMessageBase):

    def __init__(self, message):
        """
        文本消息
        :return:
        """
        self.content = message.pop("Content", "")
        super(WXAccessTextMessage, self).__init__(message)


@message_type("image")
class WXAccessImageMessage(WXAcceptMessageBase):

    def __init__(self, message):
        """
        图片消息
        :param message:
        :return:
        """
        self.pic_url = message.pop("PicUrl", "")
        self.media_id = message.pop("MediaId", "")
        super(WXAccessImageMessage, self).__init__(message)


@message_type("voice")
class WXAccessVoiceMessage(WXAcceptMessageBase):

    def __init__(self, message):
        """
        语音消息
        :param message:
        :return:
        """
        self.media_id = message.pop("MediaId", "")
        self.format = message.pop("Format", "")
        super(WXAccessVoiceMessage, self).__init__(message)


@message_type('video')
class WXAccessVideoMessage(WXAcceptMessageBase):

    def __init__(self, message):
        """
        视频消息
        :param message:
        :return:
        """
        self.media_id = message.pop('MediaId')
        self.thumb_media_id = message.pop('ThumbMediaId')
        super(WXAccessVideoMessage, self).__init__(message)


@message_type('shortvideo')
class WXAccessShortVideoMessage(WXAcceptMessageBase):

    def __init__(self, message):
        """
        小视频消息
        :param message:
        :return:
        """
        self.media_id = message.pop('MediaId')
        self.thumb_media_id = message.pop('ThumbMediaId')
        super(WXAccessShortVideoMessage, self).__init__(message)


@message_type("location")
class WXAccessLocationMessage(WXAcceptMessageBase):

    def __init__(self, message):
        """
        位置消息
        :param message:
        :return:
        """
        location_x = message.pop("Location_X", "")
        location_y = message.pop("Location_Y", "")
        self.location = (float(location_x), float(location_y))
        self.scale = int(message.pop("Scale", 0))
        self.label = message.pop("Label", "")

        super(WXAccessLocationMessage, self).__init__(message)


@message_type("link")
class WXAccessLinkMessage(WXAcceptMessageBase):

    def __init__(self, message):
        """
        链接消息
        :param message:
        :return:
        """
        self.title = message.pop("Title", "")
        self.desc = message.pop("Description", "")
        self.url = message.pop("Url", "")

        super(WXAccessLinkMessage, self).__init__(message)


class UnknownMessage(WXAcceptMessageBase):
    def __init__(self, message):
        self.type = 'unknown'
        super(UnknownMessage, self).__init__(message)


