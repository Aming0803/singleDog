# coding=utf-8
__author__ = 'wan'

import json


class CommonApiResponse(object):

    def __init__(self, data='', msg='', success=False, count=0):
        """
        Admin api common resp
        :param data:
        :param msg:
        :param success:
        :param count:
        :return:
        """
        self.data = data
        self.msg = msg
        self.success = success
        self.count = count

    def create_params(self):
        """
        :return:
        """
        d = {}
        d.update(self.__dict__)
        return d

    def convert_to_json_str(self):
        """
        :return:
        """
        result = self.create_params()
        return json.dumps(result)