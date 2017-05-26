"""将users这个应用中的所有的表注册到xadmin中"""

import xadmin

from xadmin import views

from .models import UserProfile, EmailVerifyRecord, Banner


# 打开相应的开关，支持主题的修改
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


# 自定义页面布局
class GlobalSetting(object):
    # 自定义页面的页头和页脚
    site_title = "在线学习网后台管理系统"
    site_footer = "在线学习网"
    # 自定义导航栏的样式是可折叠的形式
    menu_style = "accordion"


class UserProfileAdmin(object):
    list_display = ('username', 'email','nickname', 'birthday', 'gender', 'address', 'phone_num', 'image',)
    search_fields = ('username', 'email','nickname', 'birthday', 'gender', 'address', 'phone_num')
    list_filter = ('username', 'email','nickname', 'address', 'phone_num')


class EmailVerifyRecordAdmin(object):
    list_display = ('email', 'send_type', 'code')
    search_fields = ['email', 'send_type']
    list_filter = ('email', 'send_type')


class BannerAdmin(object):
    list_display = ('title', 'url', 'image', 'index')
    search_fields = ('title', 'url')
    list_filter = ('title', )



xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)

xadmin.site.register(Banner, BannerAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)

xadmin.site.register(views.CommAdminView, GlobalSetting)