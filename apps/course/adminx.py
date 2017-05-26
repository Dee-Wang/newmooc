# -*- coding: utf-8 -*-
__author__ = 'Dee'
__date__ = '17-5-24 下午2:51'

"""将course这个应用中的所有的表注册到xadmin中"""

import xadmin

from .models import Course, Lesson, Video, VideoResource


class CourseAdmin(object):
    list_display = ("name","course_category", "description","detail" ,"degree", "learning_time", "learning_num", "favor_num", "click_num", "image", "add_time")
    search_fields = ("name", "learning_time", )
    list_filter = ("degree", )


class LessonAdmin(object):
    list_display = ("course", "name","add_time")
    search_fields = ("name", "course", )
    list_filter = ("course", )

class VideoAdmin(object):
    list_display = ("course", "lesson","name","add_time")
    search_fields = ("name", )
    list_filter = ("course", "lesson", )

class VideoResourceAdmin(object):
    list_display = ("course", "name","download","add_time")
    search_fields = ("name",)
    list_filter = ("course", )

xadmin.site.register(Course, CourseAdmin)

xadmin.site.register(Lesson, LessonAdmin)

xadmin.site.register(Video, VideoAdmin)

xadmin.site.register(VideoResource, VideoResourceAdmin)