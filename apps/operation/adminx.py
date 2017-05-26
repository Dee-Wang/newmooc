# -*- coding: utf-8 -*-
__author__ = 'Dee'
__date__ = '17-5-24 下午3:39'

"""将operation这个应用中的所有的表注册到xadmin中"""

import xadmin

from .models import UserWant, CourseComments, UserCourse, UserFavor, UserMessage

class UserWantAdmin(object):
    list_display = ('name', 'phone_num', 'course_name', 'add_time')
    search_fields = ('name', 'phone_num', 'course_name')
    list_filter = ('course_name', )


class CourseCommentsAdmin(object):
    list_display = ('user', 'course', 'comments', 'add_time')
    search_fields = ('user', 'course', )
    list_filter = ('user', 'course', )


class UserCourseAdmin(object):
    list_display = ('user', 'course', 'add_time')
    search_fields = ('user', 'course', )
    list_filter = ('user', 'course', )


class UserFavorAdmin(object):
    list_display = ('user', 'fav_id', 'fav_type', 'add_time')
    search_fields = ('user', )
    list_filter = ('fav_id', 'fav_type', )


class UserMessageAdmin(object):
    list_display = ('user', 'is_read', 'message', 'add_time')
    search_fields = ('user', 'message', )
    list_filter = ('is_read', )


xadmin.site.register(UserWant, UserWantAdmin )

xadmin.site.register(CourseComments, CourseCommentsAdmin )

xadmin.site.register(UserCourse, UserCourseAdmin )

xadmin.site.register(UserFavor, UserFavorAdmin )

xadmin.site.register(UserMessage, UserMessageAdmin )
