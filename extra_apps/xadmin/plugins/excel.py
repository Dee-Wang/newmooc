# -*- coding: utf-8 -*-
__author__ = 'Dee'
__date__ = '17-5-29 下午6:50'

import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader


# excel文件的导入
class ListImportExcelPlugin(BaseAdminPlugin):

    import_excel = False

    # 插件的入口函数，返回一个布尔值。当返回值为True的时候才加载这个插件
    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    # def block_top_toolbar(self, context, nodes):
    #     nodes.append(loader.render_to_string('xadmin/excel/model_list.te'))