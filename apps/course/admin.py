from django.contrib import admin

from .models import Course, Lesson,  Video, VideoResource

class CourseAdmin(admin.ModelAdmin):
    list_display = ("name","course_category", "description","detail" ,"degree", "learning_time", "learning_num", "favor_num", "click_num", "image", "add_time")
    search_fields = ("name", "learning_time", )
    list_filter = ("degree", )


class LessonAdmin(admin.ModelAdmin):
    list_display = ("course", "name","add_time")
    search_fields = ("name", "course", )
    list_filter = ("course", )


class VideoAdmin(admin.ModelAdmin):
    list_display = ("course", "lesson","name","add_time")
    search_fields = ("name", )
    list_filter = ("course", "lesson", )


class VideoResourceAdmin(admin.ModelAdmin):
    list_display = ("course", "name","download","add_time")
    search_fields = ("name",)
    list_filter = ("course", )


admin.site.register(Course, CourseAdmin )
admin.site.register(Lesson, LessonAdmin )
admin.site.register(Video, VideoAdmin )
admin.site.register(VideoResource, VideoResourceAdmin )