# coding=utf-8
from __future__ import absolute_import
from taskCelery.celery import app
from celery.utils.log import get_task_logger
from common.wx_sdk.methods import (
    create_wx_user_by_openid_method
)

logger = get_task_logger(__name__)


@app.task(name="taskCelery.tasks.create_wx_user", bind=True)
def create_wx_user(self, openid):
    """
    创建微信用户信息
    :return:
    """
    try:
        success, msg = create_wx_user_by_openid_method(openid)
    except Exception as exc:
        logger.error(u"**********推送错误:%s***********" % exc.message)
        success, msg = False, "请求异常"
    return success, msg