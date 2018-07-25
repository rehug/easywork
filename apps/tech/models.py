# -*- coding: utf-8 -*-

from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from django.contrib.auth.models import User


class RawDataTask(models.Model):
    """
    WD web类型profile日志model
    """
    profile_id = models.IntegerField(null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    command = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    is_api = models.BooleanField(default=False)
    run_flag = models.BooleanField(default=False)
    create_time = models.DateField(default=timezone.now)


class RawDataTaskForm(ModelForm):
    """
    WD web类型profile日志form
    """
    class Meta:
        model = RawDataTask
        fields = (
            'profile_id', 'start_date', 'end_date', 'command', 'email', 'is_api'
        )


class OrderStatus(models.Model):
    """
    WD订单状态model
    """
    profile_id = models.IntegerField(null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    email = models.EmailField(max_length=50)
    run_flag = models.BooleanField(default=False)
    create_time = models.DateField(default=timezone.now)


class OrderStatusForm(ModelForm):
    """
    WD订单状态form
    """
    class Meta:
        model = OrderStatus
        fields = (
            'profile_id', 'start_date', 'end_date', 'email'
        )


class RcModify(models.Model):
    """
    RC/GVP report owner model
    """
    report_key = models.IntegerField(null=False)
    owner_email = models.EmailField(max_length=50)


class RcModifyForm(ModelForm):
    """
    RC/GVP report owner form
    """
    class Meta:
        model = RcModify
        fields = ('report_key', 'owner_email')


