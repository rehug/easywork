# -*- coding: utf-8 -*-
# Create your views here.
import json

import pandas as pd
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse

from apps.easy_jobs.common.dbapi import MySqlConn
from apps.easy_jobs.common.utils import day_get
from easywork.settings import EMAIL_ERROR_USERS as error_users
from easywork.settings import EMAIL_HOST_USER as mail_from
from .api_libs.psql import ReadGvpPSql
from .api_libs.rc_api import ModifyRcReportOwner
from .models import RawDataTask, RawDataTaskForm, RcModify, RcModifyForm, \
    OrderStatus, OrderStatusForm


def login(request):
    """
    用户登录，成功后返回登录前页面
    """
    if request.user.is_authenticated:
        next_url = request.GET.get('next', '/')
        return HttpResponseRedirect(next_url)
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password')
        next_url = request.GET.get('next', '/')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            response = HttpResponseRedirect(next_url)
            response.set_cookie('username', username, 3600)
            return response
    slug = 'login'  # 渲染base class属性
    return render(request, 'auth/login.html', {'slug': slug})


@login_required(login_url='/login')
def logout(request):
    """
    用户登出，成功后返回首页
    """
    auth.logout(request)
    return HttpResponseRedirect('/')


def index(request):
    """
    首页
    """
    slug = 'index'  # 渲染base class属性
    if request.method == 'POST':
        # 联系我们表单
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if name and email and subject and message:
            subject = '[Easywork建议]' + subject
            content = """
            <p style="font-family: 'Microsoft YaHei'">
            Dears Easywork,
            <br>
            <br>
            Name: {name}
            <br>
            Email: {email}
            <br>
            Message: {message}
            <br>
            <hr>
            Sent by PythonBot.
            </p>
            """.format(
                name=name, email=email, message=message
            )
            email_obj = EmailMessage(
                subject, content, mail_from, error_users
            )
            email_obj.content_subtype = 'html'
            res = email_obj.send()
            return HttpResponseRedirect('/thanks', {'res': res})

    return render(request, 'index.html', {'slug': slug})


def thanks(request):
    """
    用户反馈后感谢页面
    """
    return render(request, 'thanks.html')


def wd_rawdata(request):
    """
    WD 网页分析类型profile日志查询
    """
    if request.method == 'POST':
        raw_data_task = RawDataTask()
        # print(request.POST)
        forms = RawDataTaskForm(request.POST, instance=raw_data_task)
        is_api = request.POST.get('is_api')
        if forms.is_valid:
            forms.is_api = True if is_api else False
            # print(forms)
            forms.save()
            slug = 'wd_tasks'
            return HttpResponseRedirect('/wd/tasks', {'slug': slug})
    slug = 'wd_rawdata'  # 渲染base class属性
    return render(request, 'wd/wd_rawdata.html', {'slug': slug})


def show_tasks(request):
    """
    WD日志查询任务
    """
    if request.method == 'GET':
        tasks = RawDataTask.objects.filter().order_by('-id')
        slug = 'wd_tasks'  # 渲染base class属性
        return render(request, 'wd/wd_tasks.html', {'tasks': tasks, 'slug': slug})


@login_required(login_url='/login')
def del_task(request):
    """
    要求登录，删除WD日志查询任务
    """
    if request.user.is_authenticated:
        _del_id = request.GET.get('id')
        _del_task = RawDataTask.objects.filter(id=_del_id)
        _del_task.delete()
        return HttpResponseRedirect('/wd/tasks')
    else:
        return HttpResponseRedirect('/login')


def read_gvp_psql(request):
    """
    postgresql任务状态监测
    """
    slug = 'gvp_tasks_monitor'  # 渲染base class属性
    if request.method == 'GET':
        table = request.GET.get('table')
        limit = request.GET.get('limit') if request.GET.get('limit') else 10
        try:
            if table:
                last_data = ReadGvpPSql(table).read_psql(limit)
                return render(request, 'psql/psql_tasks_monitor.html', {
                    'last_data': last_data, 'slug': slug
                })
            else:
                tables = ReadGvpPSql(table).show_tables()
                paginator = Paginator(tables, 10)
                page = request.GET.get('page')
                try:
                    tables = paginator.page(page)
                except PageNotAnInteger:
                    tables = paginator.page(1)
                except EmptyPage:
                    tables = paginator.page(paginator.num_pages)
                return render(request, 'psql/psql_tasks_monitor.html', {
                    'tables': tables, 'slug': slug
                })
        except Exception as e:
            return render(request, 'psql/psql_tasks_monitor.html', {
                'error': str(e), 'slug': slug
            })


@login_required(login_url='/login')
def gvp_report_key(request):
    """
    根据report name 查询 report key，并用于修改report owner
    此功能仅开放给部分人员使用，要求登录
    """
    slug = 'gvp_report_key'  # 渲染base class属性
    if request.user.is_authenticated:
        if request.method == 'POST':
            report_name = request.POST.get('report_name', '-')
            rc_gvp = request.POST.get('rc_gvp')
            if report_name != '-':
                report_info = ModifyRcReportOwner(
                    0, '', rc_gvp
                ).get_report_key(report_name)
                if report_info:
                    return render(request, 'gvp/gvp_report_key.html', {
                        'report_info': report_info, 'slug': slug
                    })
                else:
                    error_info = ['Report Name does not exists. Please have a check.']
                    return render(request, 'gvp/gvp_report_key.html', {
                        'error_info': error_info, 'slug': slug
                    })

    return render(request, 'gvp/gvp_report_key.html', {'slug': slug})


@login_required(login_url='/login')
def gvp_owner(request):
    """
    根据查询到的report key修改owner
    此功能仅开放给部分人员使用，要求登录
    """
    slug = 'gvp_owner'  # 渲染base class属性
    if request.user.is_authenticated:
        if request.method == 'POST':
            rc_gvp = request.POST.get('rc_gvp')
            report_key = request.POST.get('report_key', '')
            owner_email = request.POST.get('owner_email', '')
            if report_key and owner_email:
                print(1)
                rc_modify = RcModify()
                rc_modify_form = RcModifyForm(request.POST, instance=rc_modify)
                if rc_modify_form.is_valid:
                    rc_modify_form.save()
                    modify_info = ModifyRcReportOwner(
                        report_key, owner_email, rc_gvp
                    ).modify_report_owner()
                    if modify_info:
                        return render(request, 'gvp/gvp_owner.html', {
                            'modify_info': modify_info, 'slug': slug
                        })
                    else:
                        modify_error = [
                            'Please check for ReportKey or Email.'
                        ]
                        return render(request, 'gvp/gvp_owner.html', {
                            'modify_error': modify_error, 'slug': slug
                        })

    return render(request, 'gvp/gvp_owner.html', {'slug': slug})


def order_status(request):
    """
    订单状态查询
    """
    if request.method == 'POST':
        order_status_form = OrderStatus()
        forms = OrderStatusForm(request.POST, instance=order_status_form)
        if forms.is_valid:
            forms.save()
            return HttpResponseRedirect('/wd/showStatusTasks')
    slug = 'wd_order_status'
    return render(request, 'wd/wd_order_status.html', {'slug': slug})


def show_status(request):
    """
    订单状态查询任务
    """
    if request.method == 'GET':
        tasks = OrderStatus.objects.filter().order_by('-id')
        slug = 'wd_order_status_tasks'
        return render(request, 'wd/wd_order_status_tasks.html', {
            'tasks': tasks, 'slug': slug
        })


@login_required(login_url='/login')
def del_status_task(request):
    """
    删除订单状态查询任务，此功能要求登录
    """
    if request.user.is_authenticated:
        _del_id = request.GET.get('id')
        _del_task = OrderStatus.objects.filter(id=_del_id)
        _del_task.delete()
        return HttpResponseRedirect('/showStatusTasks')
    else:
        return HttpResponseRedirect('/login')


def regular_job(request):
    return render(request, 'others/dataframe.html')


def wd_flag(request):
    """
    MK订单状态更新、商品属性更新API
    """
    engine = MySqlConn().get_engine()
    profile_id = request.GET.get('ProfileId')
    if not profile_id:
        resp = {'Error': 'ProfileId is needed!'}
        return HttpResponse(json.dumps(resp), content_type='application/json')
    day = request.GET.get('Day', day_get())
    sql = """
    SELECT Day, IsReady FROM DataFlag
    WHERE ProfileID={profile_id}
    AND Day={day}
    """.format(profile_id=profile_id, day=day)
    temp_frame = pd.read_sql_query(sql, con=engine)
    flag = 'Ready' if not temp_frame.empty else 'NotReady'
    resp = {'Day': day, 'Status': flag, 'ProfileId': profile_id}
    return HttpResponse(json.dumps(resp), content_type='application/json')

