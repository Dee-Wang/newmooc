"""mymooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin

from organization.views import TeacherListView, TeacherDetailView
from users.views import IndexView

from mymooc.settings import MEDIA_ROOT

urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    # 使用xadmin进行系统的后台管理
    url(r'^xadmin/', xadmin.site.urls),

    url('^$', IndexView.as_view(), name="index"),
    # 使用url分块，将每一块的URL放到一块，用到的时候使用include去获取
    url(r'^users/', include('users.urls', namespace="users")),

    # 第三方提供的验证码
    url(r'^captcha/', include('captcha.urls')),

    # 培训机构相关的页面的URL地址
    url(r'^org/', include('organization.urls', namespace="org")),

    # 课程相关的页面的URL地址
    url(r'^course/', include('course.urls', namespace="course")),

    # 教师列表页面的URL地址
    url(r'^teacher_list/$', TeacherListView.as_view(), name="teacher_list"),

    # 教师详情页面的URL地址
    url(r'^teacher_detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),

    # 处理静态文件的函数配置
    url(r'^media/(?P<path>.*)$', serve, {"document_root" : MEDIA_ROOT}),
]