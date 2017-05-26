from django.contrib import admin

from .models import CourseOrg, CityDict, Teacher

class CourseOrgAdmin(admin.ModelAdmin):
    list_display = ( 'name','city', 'category', 'description', 'favor_num', 'click_num', 'address', 'phone_num', 'image','add_time')
    search_fields = ('name', 'address', 'phone_num')
    list_filter = ('city', 'category')


class CityDictAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', )
    list_filter = ('name', )


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('organization', 'name', 'work_years', 'work_company','work_position', 'favor_num', 'click_num', 'characters', 'phone_num', 'image','add_time')
    search_fields = ('organization', 'name', )
    list_filter = ('organization', 'name', )

admin.site.register(CourseOrg, CourseOrgAdmin)
admin.site.register(CityDict, CityDictAdmin)
admin.site.register(Teacher, TeacherAdmin)
