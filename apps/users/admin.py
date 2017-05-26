from django.contrib import admin

from .models import UserProfile, EmailVerifyRecord, Banner

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','nickname', 'birthday', 'gender', 'address', 'phone_num', 'image',)
    search_fields = ('username', 'email','nickname', 'birthday', 'gender', 'address', 'phone_num')
    list_filter = ('username', 'email','nickname', 'address', 'phone_num')


class EmailVerifyRecordAdmin(admin.ModelAdmin):
    list_display = ('email', 'send_type', 'code')
    search_fields = ['email', 'send_type']
    list_filter = ('email', 'send_type')


class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'image', 'index')
    search_fields = ('title', 'url')
    list_filter = ('title', )

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
admin.site.register(Banner, BannerAdmin)
