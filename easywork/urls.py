# -*- coding: utf-8 -*-
"""easywork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from apps.blog import views as blog_view
from apps.tech import views as tech_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', tech_view.index),
    url(r'^thanks$', tech_view.thanks),
    url(r'^wd/rawdata/$', tech_view.wd_rawdata),
    url(r'^wd/tasks/$', tech_view.show_tasks),
    url(r'^wd/delTask/$', tech_view.del_task),
    url(r'^wd/delStatusTask/$', tech_view.del_status_task),
    url(r'^wd/isReady/$', tech_view.wd_flag),

    url(r'^psql/table/$', tech_view.read_gvp_psql),
    url(r'^gvp/reportKey$', tech_view.gvp_report_key),
    url(r'^gvp/modifyOwner$', tech_view.gvp_owner),
    url(r'^login/$', tech_view.login),
    url(r'^logout/$', tech_view.logout),
    url(r'^wd/orderStatus/$', tech_view.order_status),
    url(r'^wd/showStatusTasks/$', tech_view.show_status),
    url(r'^job/regular/$', tech_view.regular_job),
    url(r'^blog/users/$', blog_view.blog),
    url(r'^blog/lists/$', blog_view.show_blog),
    url(r'^blog/users/(\d+)/$', blog_view.show_users),
    url(r'^blog/users/(\d+)/(\d+)/$', blog_view.show_user_blog),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^project/users/$', blog_view.show_project_user),
    url(r'^project/$', blog_view.show_project),
    url(r'^project/detail/$', blog_view.show_project_detail),
]

admin.site.site_header = 'Easywork管理后台'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
