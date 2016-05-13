# coding=utf-8
__author__ = 'wan'

import json
import traceback
import logging
log = logging.getLogger(__file__)



class myPageTool(object):

    def __init__(self, data="", count=""):
        """
        将类转为page类
        :param data: 展示数据
        :param count: 数据总数
        :return:
        """
        self.data = data
        self.count = count


    def convert_to_json_str(self):
        """
        :return:
        """
        try:
            return json.dumps(self.__dict__)
        except Exception:
            log.error(traceback.format_exc())
            return json.dumps({'data':'', 'count':''})