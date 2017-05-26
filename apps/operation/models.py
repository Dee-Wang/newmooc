# _*_coding:utf-8_*_
from datetime import datetime

from django.db import models
from users.models import UserProfile
from course.models import Course


class UserWant(models.Model):
    name = models.CharField(max_length=20, verbose_name="姓名")
    phone_num = models.CharField(max_length=11, verbose_name="手机号码")
    course_name = models.CharField(max_length=16, verbose_name="课程名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return '{0}({1})'.format(self.name, self.course_name)

    class Meta:
        verbose_name = "我要学习"
        verbose_name_plural = verbose_name


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户名")
    course = models.ForeignKey(Course, verbose_name="课程名称")
    comments = models.CharField(max_length=64, verbose_name="评论内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return '({0},{1}){2}'.format(self.user, self.course, self.comments)

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户名")
    course = models.ForeignKey(Course, verbose_name="课程名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return '{0}({1})'.format(self.user, self.course)

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name


class UserFavor(models.Model):
    """用户收藏fav_type用来表示是收藏内容的类型，而fav_id表示的是收藏的这个类型的对象的id"""
    user = models.ForeignKey(UserProfile, verbose_name="用户名")
    fav_id = models.IntegerField(default=0, verbose_name="数据编号")
    fav_type = models.IntegerField(choices=((1,"课程"), (2, "课程机构"), (3, "讲师")), default=1, verbose_name="收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return '{0}({1})'.format(self.user, self.fav_type)

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    # 如果是0表示是全局的消息(也就是发给所有注册用户额的消息)，如果不是0表示的是系统发给用户个人的消息
    user = models.IntegerField(default=0, verbose_name="发送类型或者接收用户ID")
    is_read = models.BooleanField(default=False, verbose_name="是否已读")
    message = models.TextField(verbose_name="用户消息")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return '{0}({1})'.format(self.user, self.message)

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name
