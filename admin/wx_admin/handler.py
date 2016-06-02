#coding=utf-8
__author__ = 'wan'

from common.handlers.admin_base_handler import AdminBaseHandler
from common.utils.auth_util import admin_authenticated
from common.utils.date_util import get_part_time
from common.utils.api_resp_util import CommonApiResponse
from common.wx_sdk.methods import (
    create_custom_menu_method, upload_the_image_method, wx_add_temp_media_method, wx_add_permanent_other_media_method,
    wx_upload_message_news_method, wx_send_all_news_by_tag, wx_send_all_news_by_openid
)
from common.wx_sdk.config import WX_UPLOAD_IMAGE_TYPE
from services.wx_service import (
    WXMenuService, WXReplyService, WXUploadImgService, WXArticleService, WXMediaService, WXMessageRecordService
)

import os
import logging
log = logging.getLogger(__file__)


class WXConfigIndexHandler(AdminBaseHandler):

    _Template_Name = "wx_admin/config_list.html"

    @admin_authenticated
    def get(self):
        """
        微信配置首页列表
        :return:
        """
        return self.render(self._Template_Name)


class WXMenuListHandler(AdminBaseHandler):

    _Template_Name = "wx_admin/menu_list.html"

    @admin_authenticated
    def get(self):
        """
        微信自定义菜单管理列表
        :return:
        """
        page_no = self.get_argument("page", 1)
        page_size = self.get_argument('page_size', 12)

        wx_menu_ser = WXMenuService()
        menu_list, count = wx_menu_ser.get_menu_list_by_page(page_no=page_no, page_size=page_size)
        pages = self.get_total_pages(page_size, count)

        return self.render(self._Template_Name, menu_list=menu_list, pages=pages)

    def get_total_pages(self, page_size, count):
        """
        获取总页面数
        :param page_size:每页的数量
        :param count: 总数量
        :return:
        """
        if count == 0:
            return 0
        else:
            if count % page_size == 0:
                return count/page_size
            else:
                return count/page_size + 1


class WXMenuEditHandler(AdminBaseHandler):

    _Template_Name = "wx_admin/menu_editor.html"

    @admin_authenticated
    def get(self):
        """
        菜单详情或添加页面
        :return:
        """
        menu_id = self.get_argument("id", "")

        #ps.menu_id存在则是更新,反之为添加
        if not menu_id:
            return self.render(self._Template_Name, wx_menu="", msg="", menu_id=menu_id)

        wx_menu_ser = WXMenuService()
        wx_menu = wx_menu_ser.get_menu_by_id(menu_id)

        return self.render(self._Template_Name, wx_menu=wx_menu, msg="", menu_id=menu_id)


    @admin_authenticated
    def post(self):
        """
        添加
        :return:
        """
        ajax_resp = CommonApiResponse()

        menu_id = self.get_argument("menu_id", "")
        name = self.get_argument("name", "")
        category = int(self.get_argument("category"))
        menu_type = self.get_argument("menu_type")
        value = self.get_argument("value", "")
        parent_id = self.get_argument("parent_id", "")

        if not name or not value:
            ajax_resp.msg = "输入框不能为空值"
            return self.write(ajax_resp.convert_to_json_str())

        wx_menu_ser = WXMenuService()
        if menu_id:
            success, msg = wx_menu_ser.update_menu_info_by_id(menu_id, name=name, category=category, menu_type=menu_type, value=value, parent_id=parent_id)
        else:
            success, msg = wx_menu_ser.create_menu_by_params(name=name, category=category, menu_type=menu_type, value=value, parent_id=parent_id)
            if success:
                new_menu_id = msg
                msg = "创建成功"
                wx_menu_ser.update_menu_info_by_id(new_menu_id, parent_id=new_menu_id)

        ajax_resp.success, ajax_resp.msg = success, msg
        return self.write(ajax_resp.convert_to_json_str())


class WXMenuParentListHandler(AdminBaseHandler):

    _Template_Name = "wx_admin/ajax/menu_list.html"

    @admin_authenticated
    def get(self):
        """
        一级菜单列表
        :return:
        """
        menu_id = self.get_argument("id", "")

        wx_menu_ser = WXMenuService()
        if menu_id:
            wx_menu = wx_menu_ser.get_menu_by_id(menu_id)
        else:
            wx_menu = ""

        parent_menu_list = wx_menu_ser.get_parent_menu_list()

        return self.render(self._Template_Name, parent_menu_list=parent_menu_list, wx_menu=wx_menu)


class WXMenuDeleteHandler(AdminBaseHandler):

    _Template_Name = "wx_admin/common_result.html"

    @admin_authenticated
    def get(self):
        """
        删除
        :return:
        """
        title = "菜单删除"

        menu_id =self.get_argument("id", "")
        if not menu_id:
            success, msg = False, "数据异常,ID不存在"
            return self.render(self._Template_Name, success=success, msg=msg, title=title)

        wx_menu_ser = WXMenuService()
        success, msg = wx_menu_ser.update_menu_info_by_id(menu_id, deleted=True)

        return self.render(self._Template_Name, success=success, msg=msg, title=title)


class WXCreateMenuHandler(AdminBaseHandler):

    _Template_Name = "wx_admin/common_result.html"

    @admin_authenticated
    def get(self):
        """
        生成公众号的菜单数据
        :return:
        """
        title = "公众号菜单生成结果"
        success, msg = create_custom_menu_method()

        return self.render(self._Template_Name, success=success, msg=msg, title=title)


class WXReplyListHandler(AdminBaseHandler):

    _Template_Name = "wx_admin/reply_list.html"

    @admin_authenticated
    def get(self):
        """
        回复列表
        :return:
        """
        page_no = self.get_argument("page", 1)
        page_size = self.get_argument('page_size', 12)

        wx_config_ser = WXReplyService()
        reply_list, count = wx_config_ser.get_reply_list_by_page(page_no=page_no, page_size=page_size)
        pages = self.get_total_pages(page_size, count)

        return self.render(self._Template_Name, reply_list=reply_list, pages=pages)

    def get_total_pages(self, page_size, count):
        """
        获取总页面数
        :param page_size:每页的数量
        :param count: 总数量
        :return:
        """
        if count == 0:
            return 0
        else:
            if count % page_size == 0:
                return count/page_size
            else:
                return count/page_size + 1


class WXReplyEditorHandler(AdminBaseHandler):

    _Template_Name = "wx_admin/reply_editor.html"

    @admin_authenticated
    def get(self):
        """
        创建或者编辑回复规则
        :return:
        """
        reply_id = self.get_argument("reply_id", "")

        if not reply_id:
            return self.render(self._Template_Name, reply="")

        wx_reply_ser = WXReplyService()
        reply = wx_reply_ser.get_reply_by_id(reply_id)

        return self.render(self._Template_Name, reply=reply)

    @admin_authenticated
    def post(self):
        """
        :return:
        """
        ajax_resp = CommonApiResponse()

        reply_id = self.get_argument("reply_id", "")
        key = self.get_argument("key", "")
        reply_type = self.get_argument("reply_type", "")
        content = self.get_argument("content", "")

        if not key or not reply_type or not content:
            ajax_resp.msg = "参数不能为空"
            return self.write(ajax_resp.convert_to_json_str())

        wx_reply_ser = WXReplyService()
        if reply_id:
            success, msg = wx_reply_ser.update_reply_by_id(reply_id, key=key, reply_type=reply_type, content=content)
        else:
            success, msg = wx_reply_ser.create_reply_by_params(key=key, reply_type=reply_type, content=content)

        ajax_resp.success, ajax_resp.msg = success, msg
        return self.write(ajax_resp.convert_to_json_str())


class WXReplyDeleteHandler(AdminBaseHandler):

    _Template_Name = "wx_admin/common_result.html"

    @admin_authenticated
    def get(self):
        """
        删除回复
        :return:
        """
        title = "回复规则删除结果"

        reply_id = self.get_argument("reply_id", "")
        if not reply_id:
            success, msg = False, "数据异常,ID不存在"
            return self.render(self._Template_Name, success=success, msg=msg, title=title)

        wx_reply_ser = WXReplyService()
        success, msg = wx_reply_ser.update_reply_by_id(reply_id, deleted = True)
        return self.render(self._Template_Name, success=success, msg=msg, title=title)


class WXUploadImgListHandler(AdminBaseHandler):

    _Template_Name = "wx_admin/img_list.html"

    @admin_authenticated
    def get(self):
        """
        上传成功后的列表
        :return:
        """
        page_no = self.get_argument("page", 1)
        page_size = self.get_argument('page_size', 12)

        img_upload_ser = WXUploadImgService()
        img_list, count = img_upload_ser.get_upload_img_list_by_page(page_no=page_no, page_size=page_size)

        pages = self.get_total_pages(page_size, count)

        return self.render(self._Template_Name, img_list=img_list, pages=pages)


    def get_total_pages(self, page_size, count):
        """
        获取总页面数
        :param page_size:每页的数量
        :param count: 总数量
        :return:
        """
        if count == 0:
            return 0
        else:
            if count % page_size == 0:
                return count/page_size
            else:
                return count/page_size + 1


class WXImageUploadHandler(AdminBaseHandler):

    _Template_Name = "wx_admin/img_upload.html"

    @admin_authenticated
    def get(self):
        """
        微信上传图文消息内的图片获取URL
        :return:
        """
        return self.render(self._Template_Name, msg="")


    @admin_authenticated
    def post(self):
        """
        微信上传图文消息内的图片获取URL
        :return:
        """
        body = self.request.files["img"]
        if not body:
            msg = "文件不存在,请选择上传图片"
            return self.render(self._Template_Name, msg=msg)

        img = body[0]
        img_type = img["content_type"]
        img_name = img["filename"]
        if not img_type in WX_UPLOAD_IMAGE_TYPE:
            msg = "上传文件格式不支持,仅支持jpg/png格式图片"
            return self.render(self._Template_Name, msg=msg)

        file_save_path = self.save_the_upload_file(img)
        success, url = upload_the_image_method(file_save_path)
        if not success:
            msg = url
            return self.render(self._Template_Name, msg=msg)

        #ps.成功后返回的URL需要保存
        img_upload_ser = WXUploadImgService()
        success, msg = img_upload_ser.create_upload_img_by_params(source=img_name, url=url, source_path=file_save_path)
        if not success:
            return self.render(self._Template_Name, msg=msg)

        return self.redirect("/admin/wx/img/list")

    def save_the_upload_file(self, file):
        """
        保存上传的文件
        :param file:
        :return:
        """
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        target_path = os.path.join(BASE_DIR, "static/upload/images")
        if not os.path.exists(target_path):
            os.mkdir(target_path)

        target_name = os.path.join(target_path, file["filename"])
        with open(target_name, "wb") as f:
            f.write(file["body"])

        return target_name


class WXUploadImgDetailHandler(AdminBaseHandler):

    _Template_Name = "wx_admin/img_detail.html"

    @admin_authenticated
    def get(self):
        """
        微信上传图文消息内的图片获取URL--详情
        :return:
        """
        img_id = self.get_argument("img_id", "")
        if not img_id:
            msg = "数据异常,图片ID不存在"
            return self.render(self._Template_Name, msg=msg, img="")

        img_upload_ser = WXUploadImgService()
        img = img_upload_ser.get_upload_img_by_id(img_id=img_id)
        return self.render(self._Template_Name, msg="", img=img)


class WXArticleListHandler(AdminBaseHandler):

    _Template_Name = "wx_admin/article_list.html"

    @admin_authenticated
    def get(self):
        """
        图文 文章列表
        :return:
        """
        page_no = self.get_argument("page", 1)
        page_size = self.get_argument('page_size', 12)

        article_ser = WXArticleService()
        article_list, count = article_ser.get_article_list_by_page(page_size=page_size, page_no=page_no)

        pages = self.get_total_pages(page_size, count)
        return self.render(self._Template_Name, article_list=article_list, pages=pages)

    def get_total_pages(self, page_size, count):
        """
        获取总页面数
        :param page_size:每页的数量
        :param count: 总数量
        :return:
        """
        if count == 0:
            return 0
        else:
            if count % page_size == 0:
                return count/page_size
            else:
                return count/page_size + 1


class WXAddArticleHandler(AdminBaseHandler):

    _Template_Name = "wx_admin/article_add.html"

    @admin_authenticated
    def get(self):
        """
        添加
        :return:
        """
        wx_media_ser = WXMediaService()
        media_list = wx_media_ser.get_permanent_thumb_media_list()
        return self.render(self._Template_Name, media_list=media_list)

    @admin_authenticated
    def post(self):
        """
        添加图文
        :return:
        """
        ajax_resp = CommonApiResponse()

        title = self.get_argument("title", "")
        author = self.get_argument("author", "")
        digest = self.get_argument("digest", "")
        content_source_url = self.get_argument("content_source_url", "")
        thumb_media_id = self.get_argument("thumb_media_id", "")
        show_cover_pic = int(self.get_argument("show_cover_pic", "1"))
        content = self.get_argument("content", "")

        if not title or not author or not digest or not content_source_url or not thumb_media_id or not show_cover_pic or not content:
            ajax_resp.msg = "参数不能为空,请认真填写"
            return self.write(ajax_resp.convert_to_json_str())

        wx_article_ser = WXArticleService()
        ajax_resp.success, ajax_resp.msg = wx_article_ser.create_article_by_params(title=title, author=author, digest=digest, content=content,
                                                               content_source_url=content_source_url, thumb_media_id=thumb_media_id, show_cover_pic=show_cover_pic)
        return self.write(ajax_resp.convert_to_json_str())


class WXMediaListHandler(AdminBaseHandler):

    _Template_Name = "wx_admin/media_list.html"

    @admin_authenticated
    def get(self):
        """
        素材列表
        :return:
        """
        page_no = self.get_argument("page", 1)
        page_size = self.get_argument('page_size', 12)

        wx_media_ser = WXMediaService()
        media_list, count = wx_media_ser.get_admin_media_list_by_page(page_no=page_no, page_size=page_size)
        pages = self.get_total_pages(page_size, count)

        return self.render(self._Template_Name, media_list=media_list, pages=pages)

    def get_total_pages(self, page_size, count):
        """
        获取总页面数
        :param page_size:每页的数量
        :param count: 总数量
        :return:
        """
        if count == 0:
            return 0
        else:
            if count % page_size == 0:
                return count/page_size
            else:
                return count/page_size + 1


class WXAddTempMediaHandler(AdminBaseHandler):

    _Template_Name = "wx_admin/temp_media_upload.html"

    @admin_authenticated
    def get(self):
        """
        临时素材上传
        :return:
        """
        return self.render(self._Template_Name, msg="")

    @admin_authenticated
    def post(self):
        """
        :return:
        """
        media_type = self.get_argument("type")
        body = self.request.files["source"]
        if not body:
            msg = "文件不存在,请选择素材"
            return self.render(self._Template_Name, msg=msg)

        media = body[0]
        media_name = media["filename"]
        file_save_path = self.save_the_upload_file(media)
        success, content = wx_add_temp_media_method(media_type, file_save_path)

        if not success:
            msg = content
            return self.render(self._Template_Name, msg=msg)

        #ps.成功则保存
        wx_media_ser = WXMediaService()
        resp_type = content["type"]
        if resp_type == "thumb":
            media_id = content["thumb_media_id"]
        else:
            media_id = content["media_id"]
        created_at = content["created_at"]
        create_time, end_time = get_part_time(created_at)
        success, msg = wx_media_ser.create_media_by_params(source=media_name, type=media_type,
                    media_id=media_id, gmt_created=create_time, expire_time=end_time)

        if success:
            return self.redirect("/admin/wx/media/list")
        else:
            msg = "添加临时素材成功.但是,保存失败"
            return self.render(self._Template_Name, msg=msg)

    def save_the_upload_file(self, file):
        """
        保存上传的文件
        :param file:
        :return:
        """
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        target_path = os.path.join(BASE_DIR, "static/upload/media")
        if not os.path.exists(target_path):
            os.mkdir(target_path)

        target_name = os.path.join(target_path, file["filename"])
        with open(target_name, "wb") as f:
            f.write(file["body"])

        return target_name


class WXAddPermanentOtherMediaHandler(AdminBaseHandler):

    _Template_Name = "wx_admin/permanent_media_upload.html"

    @admin_authenticated
    def get(self):
        """
        添加永久其他素材
        :return:
        """
        return self.render(self._Template_Name, msg="")

    @admin_authenticated
    def post(self):
        """
        添加永久其他素材
        :return:
        """
        media_type = self.get_argument("type")
        title = self.get_argument("title", None)
        introduction = self.get_argument("introduction", None)
        body = self.request.files["source"]

        if not body:
            msg = "文件不存在,请选择素材"
            return self.render(self._Template_Name, msg=msg)

        media = body[0]
        media_name = media["filename"]
        file_save_path = self.save_the_upload_file(media)
        success, content = wx_add_permanent_other_media_method(media_type, file_save_path, title=title, introduction=introduction)

        if not success:
            msg = content
            return self.render(self._Template_Name, msg=msg)

        #ps.成功则保存
        wx_media_ser = WXMediaService()
        media_id = content["media_id"]
        url = content.get("url", "")
        success, msg = wx_media_ser.create_media_by_params(source=media_name, type=media_type,
                    media_id=media_id, url=url, category=2)

        if success:
            return self.redirect("/admin/wx/media/list")
        else:
            msg = "添加临时素材成功.但是,保存失败"
            return self.render(self._Template_Name, msg=msg)

    def save_the_upload_file(self, file):
        """
        保存上传的文件
        :param file:
        :return:
        """
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        target_path = os.path.join(BASE_DIR, "static/upload/media")
        if not os.path.exists(target_path):
            os.mkdir(target_path)

        target_name = os.path.join(target_path, file["filename"])
        with open(target_name, "wb") as f:
            f.write(file["body"])

        return target_name


class WXSendNewMessagesHandler(AdminBaseHandler):

    _Template_Name = "wx_admin/news_message.html"

    @admin_authenticated
    def get(self):
        """
        群发图文消息 上传图文
        :return:
        """
        wx_article_ser = WXArticleService()
        article_list = wx_article_ser.get_article_list()

        wx_media_ser = WXMediaService()
        media_list = wx_media_ser.get_message_news_media_list()
        return self.render(self._Template_Name, article_list=article_list, media_list=media_list)

    @admin_authenticated
    def post(self):
        """
        群发图文消息
        :return:
        """
        ajax_resp = CommonApiResponse()

        category = self.get_argument("category", "")
        is_new_media = self.get_argument("is_new_media", "")

        #ps.如果是新上传的图文
        if is_new_media == 'new':
            article_id_list = self.get_arguments("ids[]")
            success, content = wx_upload_message_news_method(article_id_list)
            if not success:
                ajax_resp.msg = content
                return self.write(ajax_resp.convert_to_json_str())

            wx_media_ser = WXMediaService()
            media_type = content["type"]
            media_id = content["media_id"]
            created_at = content["created_at"]
            create_time, end_time = get_part_time(created_at)
            source=",".join(article_id_list)
            #todo:保存返回得数据
            success, msg = wx_media_ser.create_media_by_params(type=media_type, media_id=media_id, gmt_created=create_time, expire_time=end_time,
                                                category=3, source=source)
            log.info(u"*************保存群发上传图文的结果: {0}|{1}******".format(success, msg))

        else:
            media_id = self.get_argument("media_id", "")
            if not media_id:
                ajax_resp.msg = "素材不存在,请选择群发素材"
                return self.write(ajax_resp.convert_to_json_str())

        #todo:开始群发,根据标签分组或者openid群发
        if category == 'tag':
            success, msg_data = wx_send_all_news_by_tag(media_id)
            if not success:
                ajax_resp.msg = msg_data
                return self.write(ajax_resp.convert_to_json_str())
        else:
            #category=='openid'
            success, msg_data = wx_send_all_news_by_openid(media_id)
            if not success:
                ajax_resp.msg = msg_data
                return self.write(ajax_resp.convert_to_json_str())

        #todo.保存返回的群发msg_id
        message_record_ser = WXMessageRecordService()
        msg_id = msg_data["msg_id"]
        msg_data_id = msg_data["msg_data_id"]
        success, msg = message_record_ser.create_wx_message_record_by_params(content=media_id, type="news", msg_id=msg_id, msg_data_id=msg_data_id)
        log.info(u"*************保存群发返回MSG_ID的结果: {0}|{1}******".format(success, msg))

        ajax_resp.success, ajax_resp.msg = True, "群发消息已发出"
        return self.write(ajax_resp.convert_to_json_str())


