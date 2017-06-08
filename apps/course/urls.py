from django.conf.urls import url,include

from .views import CourseListView, CourseDetailView, CourseVideoView, CourseCommentView, AddCourseCommentView, CourseVideoPlayView

urlpatterns = [
    # 课程列表页
    url(r'^course_list/$', CourseListView.as_view(), name="course_list"),

    # 课程详情界面
    url(r'^course_detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),

    # 章节视频信息页面
    url(r'^course_video/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name="course_video"),

    # 课程评论信息页面
    url(r'^course_comments/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="course_comments"),

    # # 课程播放页面
    url(r'^video_play/(?P<video_id>\d+)/$', CourseVideoPlayView.as_view(), name="video_play"),

    # 添加课程评论信息
    url(r'^add_coursecomment/$', AddCourseCommentView.as_view(), name="add_coursecomment"),
]