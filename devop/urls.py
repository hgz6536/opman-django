"""devop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from opman.views import idcinfo, idcadd_play, idcadd_data, idcdel_data, idcedit_commit, idcedit_data, userinfo, useradd_play, useradd_data, userdel_data, useredit_data, useredit_commit, \
    dashboard, register
from django.contrib import admin
from django.contrib.auth.views import login, logout, logout_then_login, password_change, password_change_done, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from devop.views.permission import *
from devop.views.user import ListUser
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # 用户注册
    url(r'^register/$', register, name='register'),

    # 登录
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^logout-then-login/$', logout_then_login, name='logout-then-login'),

    # 首页
    url(r'^$', dashboard, name='dashboard'),

    # 用户信息
    url(r'^user/list/$', ListUser, name='listuserurl'),
    url(r'^useradd_play/$', useradd_play),
    url(r'^useradd_data/$', useradd_data),
    url(r'^userdel_data/$', userdel_data),
    url(r'^useredit_data/$', useredit_data),
    url(r'^useredit_commit/$', useredit_commit),

    # 密码管理
    url(r'^password-change/$', password_change, name='password_change'),
    url(r'^password-change/done/$', password_change_done, name='password_change_done'),
    url(r'^password-reset/$', password_reset, name='password_reset'),
    url(r'^password-reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', password_reset_complete, name='password_reset_complete'),

    # 权限控制
    url(r'^permission/deny/$', Nopermisson, name='permissiondenyurl'),
    url(r'^permission/add/$', AddPermission, name='addpermissonurl'),
    url(r'^permission/list/$', ListPermission, name='listpermissionurl'),
    url(r'^permission/edit/(?P<ID>\d+)/$', EditPermission, name='editpermissionurl'),
    url(r'^permission/delete/(?P<ID>\d+)/$', DelePermission, name='deletepermissionurl'),

    # IDC机房信息管理
    url(r'^idc/$', idcinfo, name='idcinfo'),
    url(r'^idcadd_play/$', idcadd_play),
    url(r'^idcadd_data/$', idcadd_data),
    url(r'^idcdel_data/$', idcdel_data),
    url(r'^idcedit_data/$', idcedit_data),
    url(r'^idcedit_commit/$', idcedit_commit),
]

