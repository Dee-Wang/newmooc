from django.contrib import admin

from .models import UserWant, CourseComments, UserCourse, UserFavor, UserMessage

class UserWantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_num', 'course_name', 'add_time')
    search_fields = ('name', 'phone_num', 'course_name')
    list_filter = ('course_name', )


class CourseCommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'comments', 'add_time')
    search_fields = ('user', 'course', )
    list_filter = ('user', 'course', )


class UserCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'add_time')
    search_fields = ('user', 'course', )
    list_filter = ('user', 'course', )


class UserFavorAdmin(admin.ModelAdmin):
    list_display = ('user', 'fav_id', 'fav_type', 'add_time')
    search_fields = ('user', )
    list_filter = ('fav_id', 'fav_type', )


class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_read', 'message', 'add_time')
    search_fields = ('user', 'message', )
    list_filter = ('is_read', )


admin.site.register(UserWant, UserWantAdmin )
admin.site.register(CourseComments, CourseCommentsAdmin )
admin.site.register(UserCourse, UserCourseAdmin )
admin.site.register(UserFavor, UserFavorAdmin )
admin.site.register(UserMessage, UserMessageAdmin )

# Register your models here.
