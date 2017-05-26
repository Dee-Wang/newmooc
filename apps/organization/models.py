from datetime import datetime

from django.db import models


class CityDict(models.Model):
    name = models.CharField(max_length=8, verbose_name="城市名")
    description = models.CharField(max_length=32, verbose_name="城市简述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "城市信息"
        verbose_name_plural = verbose_name


class CourseOrg(models.Model):
    city = models.ForeignKey(CityDict, verbose_name="所在城市")
    name = models.CharField(max_length=16, verbose_name="课程机构名")
    category = models.CharField(max_length=32, choices=(("trainingorg", "培训机构"), ("university", "高校"), ("personal", "个人")), default="trainingorg", verbose_name="机构类别")
    description = models.TextField(verbose_name="机构简述", null=True, blank=True)
    favor_num = models.IntegerField(default=0, verbose_name="收藏人数")
    click_num = models.IntegerField(default=0, verbose_name="点击量")
    address = models.CharField(max_length=64, verbose_name="机构地址")
    phone_num = models.CharField(max_length=16, verbose_name="联系方式")
    image = models.ImageField(upload_to="organization/%Y/%m", default="organization/mooc.jpg", max_length=128, verbose_name="Logo")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    # 得到这个培训机构总的课程的数量
    def get_course_nums(self):
        return self.course_set.all().count()

    # 得到某个培训机构的讲师的数量
    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    organization = models.ForeignKey(CourseOrg, verbose_name="所属机构")
    name = models.CharField(max_length=16, verbose_name="讲师名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=32, verbose_name="供职单位", null=True, blank=True)
    work_position = models.CharField(max_length=16, verbose_name="公司职位", null=True, blank=True)
    characters = models.TextField(verbose_name="讲师风格", null=True, blank=True)
    favor_num = models.IntegerField(default=0, verbose_name="收藏人数")
    click_num = models.IntegerField(default=0, verbose_name="点击量")
    phone_num = models.CharField(max_length=16, verbose_name="联系方式")
    image = models.ImageField(upload_to="organization/teahers/%Y/%m", default="organization/teachers/default.png", max_length=128,
                              verbose_name="讲师照片")
    age = models.IntegerField(default=0, verbose_name="年龄")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    # 获得该讲师的所有课程的一个集合,返回值的类型是QuerySet类型
    def get_teacher_course(self):
        return self.course_set.all()

    # 获得这个讲师的课程数, 返回值的类型是整型数
    def get_teacher_course_num(self):
        return self.course_set.all().count()

    class Meta:
        verbose_name = "讲师信息"
        verbose_name_plural = verbose_name
