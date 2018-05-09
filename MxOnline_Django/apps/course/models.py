# _*_ encoding:utf-8 _*_
from django.db import models
from datetime import datetime
# Create your models here.

from organization.models import CourseOrg,Teacher

class Course(models.Model):
    CourseOrg = models.ForeignKey(CourseOrg, verbose_name="课程机构", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    des = models.CharField(max_length=500,verbose_name=u'课程描述')
    degree = models.CharField(max_length=2, choices=(("cj", u"初级"), ("zj", "中级"),("gj", "高级")),verbose_name=u'难度')
    learn_times = models.IntegerField(default=0,verbose_name=u'学习时长(分钟数)')
    students = models.IntegerField(default=0,verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name=u'收藏人数')
    image = models.ImageField(upload_to="course/%Y/%m",verbose_name=u'封面图', max_length=100)
    click_nums = models.IntegerField(default=0,verbose_name=u'点击数')
    tag = models.CharField(default='',max_length=10, verbose_name=u'课程标签')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')
    category = models.CharField(default="后端",max_length=50,verbose_name=u'课程类别')
    is_banner = models.BooleanField(default=False,verbose_name='是否轮播')
    teacher = models.ForeignKey(Teacher,verbose_name='讲师',null=True,blank=True)
    youneed_know = models.CharField(default="", max_length=300,verbose_name=u'课程须知')
    teacher_tell = models.CharField(default="", max_length=300,verbose_name=u'老师告诉你')
    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        #获取课程章节数
        return self.lesson_set.all().count()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        #获取课程所有章节
        return self.lesson_set.all()

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

    def get_lesson_vedio(self):
        #获取章节视频
        return self.video_set.all()



class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    url = models.CharField(max_length=200,default='', verbose_name=u"访问地址")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class CourseResoure(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="course/%Y/%m",verbose_name=u"资源文件",max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name