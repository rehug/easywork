# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from apps.blog.models import WeekReport, User, Project, ProjectUser


def blog(request):
    slug = 'weekly'
    users = User.objects.all()
    return render(request, 'blog/week_report.html', {
        'users': users, 'slug': slug
    })


def show_users(request, uid):
    slug = 'weekly'
    username = User.objects.filter(id=uid)
    blogs = WeekReport.objects.filter(user_id=uid)
    return render(request, 'blog/user_blog_list.html', {
        'blogs': blogs, 'username': username, 'slug': slug
    })


def show_user_blog(request, uid, bid):
    slug = 'weekly'
    blg = WeekReport.objects.filter(id=bid)
    return render(request, 'blog/blog.html', {
        'blog': blg, 'slug': slug
    })


def show_blog(request):
    blg = WeekReport.objects.all().order_by('-edit_time')
    slug = 'faq'
    return render(request, 'blog/blog_lists.html', {
        'blgs': blg, 'slug': slug
    })


@login_required(login_url='/login')
def show_project_user(request):
    if request.user.is_authenticated:
        project_users = ProjectUser.objects.all()
        slug = 'project'
        return render(request, 'blog/project_users.html', {
            'project_users': project_users, 'slug': slug
        })
    return HttpResponseRedirect('/login')


@login_required(login_url='/login')
def show_project(request):
    if request.user.is_authenticated:
        projects = Project.objects.all().order_by('-edit_time')
        paginator = Paginator(projects, 10)
        page = request.GET.get('page')
        slug = 'project'
        try:
            projects = paginator.page(page)
        except PageNotAnInteger:
            projects = paginator.page(1)
        except EmptyPage:
            projects = paginator.page(paginator.num_pages)
        return render(request, 'blog/projects.html', {
            'projects': projects, 'slug': slug
        })
    return HttpResponseRedirect('/login')


@login_required(login_url='/login')
def show_project_detail(request):
    if request.user.is_authenticated:
        slug = 'project'
        pid = request.GET.get('pid')
        project = Project.objects.filter(id=pid)
        return render(request, 'blog/project_detail.html', {
            'project': project, 'slug': slug
        })
    return HttpResponseRedirect('/login')




