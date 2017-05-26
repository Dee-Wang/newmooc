from django.conf.urls import url,include

from .views import OrgView, AdduserwantView, OrgHomeView, OrgCourseView, OrgDescriptionView, OrgTeacherView, AddFavView

urlpatterns = [
    # 课程机构列表页
    url(r'^org_list/$', OrgView.as_view(), name="org_list"),

    # 我要学习
    url(r'^adduserwant/$',AdduserwantView.as_view(), name="adduserwant"),

    # 用户收藏培训机构
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

    # 机构首页
    url(r'^org_home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),

    # 机构中的课程列表页
    url(r'^org_course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),

    # 机构简述页面
    url(r'^org_description/(?P<org_id>\d+)/$', OrgDescriptionView.as_view(), name="org_description"),

    # 机构讲师页面
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),
]