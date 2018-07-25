# -*- coding: utf-8 -*-

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.name


class WeekReport(models.Model):
    subject = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    content = RichTextUploadingField()
    edit_time = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.subject


class ProjectUser(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.name


class ProjectType(models.Model):
    project_type = models.CharField(max_length=50, default='项目相关')

    def __str__(self):
        return self.project_type


class ProjectName(models.Model):
    project_name = models.CharField(max_length=50)

    def __str__(self):
        return self.project_name


class Project(models.Model):
    type_choices = (
        ('1', '项目相关'),
        ('2', '学习相关'),
        ('3', '其他任务'),
    )
    project_type = models.ForeignKey(ProjectType, verbose_name='项目类型')
    project_name = models.ForeignKey(ProjectName, verbose_name='项目名称')
    subject = models.CharField(max_length=100, verbose_name='标题')
    project_user = models.ForeignKey(ProjectUser, verbose_name='人员')
    paid_day = models.IntegerField(default=0, verbose_name='耗费天数')
    paid_hour = models.IntegerField(default=0, verbose_name='耗费小时数')
    paid_quarter = models.IntegerField(default=0, verbose_name='耗费刻数')
    content = RichTextUploadingField(verbose_name='正文')
    edit_time = models.DateTimeField(default=timezone.now(), verbose_name='编辑时间')

    def __str__(self):
        return self.subject




