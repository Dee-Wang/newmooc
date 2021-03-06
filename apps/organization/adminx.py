# -*- coding: utf-8 -*-
__author__ = 'Dee'
__date__ = '17-5-24 下午2:47'

"""将organization这个应用中的所有的表注册到xadmin中"""

import xadmin

from .models import CourseOrg, Teacher, CityDict
from course.models import Lesson, Video, VideoResource


# 设置Lesson的inline
class LessonInline(object):
    model = Lesson
    extra = 0


class CourseOrgAdmin(object):
    list_display = ( 'name','city', 'category', 'description', 'favor_num', 'click_num', 'address', 'phone_num', 'image','add_time', 'get_course_nums', 'go_to')
    search_fields = ('name', 'address', 'phone_num')
    list_filter = ('city', 'category')
    relfield_style = 'fk-ajax'
    inlines = [LessonInline]


class TeacherAdmin(object):
    list_display = ('name', 'characters')
    search_fields = ('name', )
    list_filter = ('name', )
    relfield_style = 'fk-ajax'


class CityDictAdmin(object):
    list_display = ('organization', 'name', 'work_years', 'work_company','work_position', 'favor_num', 'click_num', 'characters', 'phone_num', 'image','add_time')
    search_fields = ('organization', 'name', )
    list_filter = ('organization', 'name', )

xadmin.site.register(CourseOrg, CourseOrgAdmin)

xadmin.site.register(Teacher, TeacherAdmin)

xadmin.site.register(CityDict, CityDictAdmin)