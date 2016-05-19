# coding=utf-8
__author__ = 'wan'


def modelObj2Dict(obj):
    """
    wms 对象转换为字典
    :param obj:
    :return:
    """
    d = {}
    field_list = obj.get_model_fields()
    for field in field_list:
        value = getattr(obj, field)
        if value:
            d.update({field: value})
        else:
            continue

    return d


class ObjectDict(dict):
    """
    dict use like object
    """
    def __getattr__(self, item):
        if item in self:
            return self[item]
        return None

    def __setattr__(self, key, value):
        self[key] = value




if __name__ == '__main__':
    test = {'a':1, "b":2}
    new_obj = ObjectDict(test)
    print new_obj.a