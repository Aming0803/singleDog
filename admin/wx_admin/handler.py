#coding=utf-8
__author__ = 'wan'

from common.handlers.admin_base_handler import AdminBaseHandler
from common.utils.auth_util import admin_authenticated
from common.utils.api_resp_util import CommonApiResponse
from common.wx_sdk.methods import create_custom_menu_method
from services.wx_service import WXMenuService


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

        return self.render(self._Template_Name, menu_list=menu_list, pages=pages, number=page_no)

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
                wx_menu_ser.update_menu_info_by_id(new_menu_id, parent_id=new_menu_id)

        ajax_resp.success, ajax_resp.msg = success, "创建成功" if success else msg
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
        menu_id =self.get_argument("id")
        wx_menu_ser = WXMenuService()
        success, msg = wx_menu_ser.update_menu_info_by_id(menu_id, deleted=True)
        title = "菜单删除"

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