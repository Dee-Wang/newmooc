from datetime import datetime

from django.db import models

from DjangoUeditor.models import UEditorField

from organization.models import CourseOrg, Teacher


# 课程数据表
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name="所属机构", null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name="授课讲师", null=True, blank=True)
    course_category = models.CharField(max_length=64, verbose_name="课程类别")
    is_banner = models.BooleanField(default=False, verbose_name="是否轮播")
    name = models.CharField(max_length=64, verbose_name="课程名")
    description = models.CharField(max_length=32, verbose_name="课程简述")
    # detail = UEditorField(verbose_name='课程详情',width=600, height=300, imagePath="course/Ueditor/",
    #                       filePath="course/Ueditor/", default='')
    detail = models.TextField(verbose_name="课程详情", default='')
    course_notice = models.TextField(verbose_name="课程须知")
    course_gain = models.TextField(verbose_name="你将学到", null=True, blank=True)
    course_tag = models.CharField(max_length=64, default='', verbose_name='课程标签')
    degree = models.CharField(max_length=10, choices=(("easy","初级"), ("nomal","中级"), ("tough","高级")), default="easy", verbose_name="难度")
    learning_time = models.IntegerField(default=0, verbose_name="课程时长(单位:分钟)")
    learning_num = models.IntegerField(default=0, verbose_name="学习人数")
    favor_num = models.IntegerField(default=0, verbose_name="收藏人数")
    click_num = models.IntegerField(default=0, verbose_name="点击量")
    image = models.ImageField(upload_to="course/%Y/%m", default="course/default.png", max_length=128, verbose_name="课程封面")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    # 获取当前的课程下面的所有章节
    def get_lesson(self):
        return self.lesson_set.all()

    # 获取课某课程下章节数的方法
    def get_lesson_nums(self):
        return self.lesson_set.all().count()

    # 获取学习该课程的学员信息，这里可以设置获取的数量
    # 但是在这里计算的话效率比较低，因为每次进入课程详情页面都得遍历计算一次
    # def get_learn_users(self):
    #     return self.usercourse_set.all()[:5]

    # # 获取当前课程的学习人数
    # def get_learning_num(self):
    #     return self.usercourse_set.all().count()

    # 获取学习当前的课程的人还在学习的其他的课程
    def get_curcourseuser_othercourse(self):
        cur_course_user = self.usercourse_set.all[:5]
        sameuser_learn_courses = []
        if cur_course_user:
            for user in cur_course_user:
                sameuser_learn_courses += self.usercourse_set.all()
            else:
                sameuser_learn_courses += []

        return sameuser_learn_courses[:5]

    # 获取当前课程的所有的视频资源信息
    def get_video_resources(self):
        return self.videoresource_set.all()

    # 获取当前课程的所有的评论内容
    def get_course_comments(self):
        return self.coursecomments_set.all()

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name


# 轮播的课程数据表
class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        proxy = True


# 章节信息数据表
class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name="所属课程")
    name = models.CharField(max_length=64, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    # 获取当前章节视频信息
    def get_lesson_video(self):
        return self.video_set.all()

    class Meta:
        verbose_name = "章节信息"
        verbose_name_plural = verbose_name


# 视频信息数据表
class Video(models.Model):
    course = models.ForeignKey(Course, verbose_name="所属课程")
    lesson = models.ForeignKey(Lesson, verbose_name="所属章节")
    name = models.CharField(max_length=128, verbose_name="视频名称")
    url = models.URLField(max_length=200, default='', verbose_name="访问地址")
    learning_time = models.IntegerField(default=0, verbose_name="学习时长(单位:分钟)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "视频信息"
        verbose_name_plural = verbose_name


# 视频资源信息数据表
class VideoResource(models.Model):
    course = models.ForeignKey(Course, verbose_name="所属课程")
    name = models.CharField(max_length=16, verbose_name="资源名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name="下载地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name
