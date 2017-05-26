from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=16, verbose_name="昵称", default=" ")
    birthday = models.DateTimeField(verbose_name="出生日期", null=True, blank=True)
    gender = models.CharField(max_length=8, choices=(("male","先生"), ("female","女士")), default="male",verbose_name="性别")
    address = models.CharField(max_length=32, verbose_name="地址",default=" ", null=True, blank=True)
    phone_num = models.CharField(max_length=11, verbose_name="手机号码")
    image = models.ImageField(upload_to="image/%Y/%m", default="image/superman.jpg", max_length=128, verbose_name="用户头像")

    def __str__(self):
        return self.username

    # 获取当前用户的所有学习课程
    def get_usr_course(self):
        return self.usercourse_set.all()

    # 获取当前的用户所有的学习课程的数目
    def get_user_course_num(self):
        return self.usercourse_set.all().count()

    # 获取当前用户收藏的所有的课程
    def get_user_favcourse(self):
        return self.userfavor_set.filter(fav_type=1).all()

    # 获取当前用户收藏的所有课程的数量
    def get_user_favcourse_num(self):
        return self.userfavor_set.filter(fav_type=1).all().count()

    # 获取当前用户收藏的所有的讲师
    def get_user_favteacher(self):
        return self.userfavor_set.filter(fav_type=3).all()

    # 获取当前用户收藏的所有讲师的数量
    def get_user_favteacher_num(self):
        return self.userfavor_set.filter(fav_type=3).all().count()

    # 获取当前用户收藏的所有的培训机构
    def get_user_favorg(self):
        return self.userfavor_set.filter(fav_type=2).all()

    # 获取当前用户收藏的所有讲师的数量
    def get_user_favorg_num(self):
        return self.userfavor_set.filter(fav_type=2).all().count()


    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=16, verbose_name="验证码")
    email = models.CharField(max_length=32, verbose_name="邮箱")
    send_type = models.CharField(max_length=64, choices=(("register","注册"), ("forget_password","忘记密码"),("change_email","修改邮箱")), default="register", verbose_name="验证类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    def __str__(self):
        return '{0}({1})'.format(self.code,self.email)

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name
        verbose_name_plural = verbose_name


class Banner(models.Model):
    title = models.CharField(max_length=20, verbose_name="标题")
    image = models.ImageField(upload_to="image/%Y/%m", default="image/default.png", max_length=128, verbose_name="封面图")
    url = models.URLField(max_length=200, verbose_name="访问地址")
    index = models.IntegerField(default=100, verbose_name="顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

