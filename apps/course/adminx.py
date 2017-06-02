# -*- coding: utf-8 -*-
__author__ = 'Dee'
__date__ = '17-5-24 下午2:51'

"""将course这个应用中的所有的表注册到xadmin中"""

import xadmin

from .models import Course, BannerCourse, Lesson, Video, VideoResource


# 注册非轮播课程数据表到后台
class CourseAdmin(object):
    list_display = ("name","course_category", "description","detail" ,"degree", "learning_time", "learning_num", "favor_num", "click_num", "image", "add_time")
    search_fields = ("name", "learning_time", )
    list_filter = ("degree", )
    ordering = ['-click_num']
    readonly_fields = ["learning_num","favor_num", "click_num" ]
    # exclude = ["learning_time"]
    list_editable = ["degree","course_category","image",]
    refresh_times = [3,5]


    # 获取非轮播课程的课程
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    # # 每次发生变化都要重新保存下这个数据表
    # def save_model(self):
    #     obj = self.new_obj
    #     course_org = obj.course_org
    #     course_org.course


# 注册轮播课程数据表到后台管理系统
class BannerCourseAdmin(object):
    list_display = ("name","course_category", "description","detail" ,"degree", "learning_time", "learning_num", "favor_num", "click_num", "image", "add_time")
    search_fields = ("name", "learning_time", )
    list_filter = ("degree", )
    ordering = ['-click_num']
    readonly_fields = ["learning_num","favor_num", "click_num" ]
    exclude = ["learning_time"]
    refresh_times = [3, 5]

    # 获取轮播课程
    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner = True)
        return qs

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


"""将所有的数据表以及对应的admin注册到后台管理中"""

xadmin.site.register(Course, CourseAdmin)

xadmin.site.register(BannerCourse, BannerCourseAdmin)

xadmin.site.register(Lesson, LessonAdmin)

xadmin.site.register(Video, VideoAdmin)

xadmin.site.register(VideoResource, VideoResourceAdmin)