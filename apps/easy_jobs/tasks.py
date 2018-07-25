#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/3 18:02
# @Author  : Ferras

import datetime
import django
django.setup()
from django.core.mail import send_mail
from celery import task

from log_writer import logger
from apps.tech.models import RawDataTask, OrderStatus as OrderStatusForm
from apps.easy_jobs.temp_wd.wd_modules import ImpalaRawDataParser, OrderStatus
from apps.easy_jobs.ua import job1, job2
from apps.easy_jobs.mk_leads import update_table as mk_update_table
from apps.easy_jobs.common import utils


@task
def wd_jobs():
    """
    WD rawdata regular job.
    :return:
    """
    tasks = RawDataTask.objects.filter(run_flag=False)
    for task_obj in tasks:
        profile_id = task_obj.profile_id
        start_date = task_obj.start_date
        end_date = task_obj.end_date
        command = task_obj.command
        to_email = task_obj.email
        is_api = task_obj.is_api

        temp_task = tasks.get(id=task_obj.id)
        temp_task.run_flag = True
        temp_task.save()

        try:
            res1 = ImpalaRawDataParser(
                profile_id, start_date, end_date, command, [to_email]
            )
            res1.send_email(is_api)
        except Exception as e:
            err_email_obj = ImpalaRawDataParser(
                profile_id, start_date, end_date, command, [to_email]
            )
            err_email_obj.error_mail(str(e))


@task
def job1():
    yesterday = int(datetime.datetime.strftime(
        datetime.datetime.today() - datetime.timedelta(days=1), "%Y%m%d"))
    input_start_day = yesterday
    input_end_day = yesterday
    try:
        job1.main(input_start_day, input_end_day)
    except Exception as e:
        logger.error(e)
        subject = 'job1 failed'
        message = 'job1 failed'
        from_email = 'example@email.com'
        send_mail(subject, message, from_email, ['example@email.com'])


@task
def job2():
    yesterday = int(datetime.datetime.strftime(
        datetime.datetime.today() - datetime.timedelta(days=1), "%Y%m%d"))
    input_start_day = yesterday
    input_end_day = yesterday
    try:
        job2.main(input_start_day, input_end_day)
    except Exception as e:
        logger.error(e)
        subject = 'job2 failed'
        message = 'job2 failed'
        from_email = 'example@email.com'
        send_mail(subject, message, from_email, ['example@email.com'])


@task
def update_table():
    from apps.easy_jobs.mk_leads import wd3_update
    today = int(datetime.datetime.strftime(
        datetime.datetime.today(), "%Y%m%d"))
    yesterday = utils.day_get(-1)
    start_day = end_day = today
    try:
        openbi_connection_string = "DSN=SampleClouderaImpalaDSN"
        mk_update_table.main(openbi_connection_string)
        for task_name in ["order_update", "product_update"]:
            task = wd3_update.main(task_name, start_day, end_day)
        wd3_update.status_update(
            profile_id=task['api_profile_id'], day=yesterday, is_ok=1)
    except Exception as e:
        logger.error(e)
        subject = 'update_table failed'
        message = 'update_table failed'
        from_email = 'example@email.com'
        send_mail(subject, message, from_email, ['example@email.com'])


@task
def order_status():
    tasks = OrderStatusForm.objects.filter(run_flag=False)
    for task_obj in tasks:
        profile_id = task_obj.profile_id
        start_date = str(task_obj.start_date)
        end_date = str(task_obj.end_date)
        to_email = task_obj.email

        temp_task = tasks.get(id=task_obj.id)
        temp_task.run_flag = True
        temp_task.save()
        try:
            res1 = OrderStatus(
                start_date, end_date, profile_id, [to_email]
            )
            res1.send_email()
        except Exception as e:
            res2 = OrderStatus(
                start_date, end_date, profile_id, [to_email]
            )
            res2.error_mail(e)
