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
from opman.views import index, idcinfo, idcadd_play, idcadd_data, idcdel_data, idcedit_commit, idcedit_data, userinfo, useradd_play, useradd_data, userdel_data, useredit_data, useredit_commit, user_login, \
    dashboard, register
from django.contrib import admin
from django.contrib.auth.views import login, logout, logout_then_login, password_change, password_change_done, password_reset, password_reset_done, password_reset_confirm, password_reset_complete

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', index),
    url(r'^idc/$', idcinfo),
    url(r'^idcadd_play/$', idcadd_play),
    url(r'^idcadd_data/$', idcadd_data),
    url(r'^idcdel_data/$', idcdel_data),
    url(r'^idcedit_data/$', idcedit_data),
    url(r'^idcedit_commit/$',idcedit_commit),
    #用户信息
    url(r'^user/$', userinfo),
    url(r'^useradd_play/$', useradd_play),
    url(r'^useradd_data/$', useradd_data),
    url(r'^userdel_data/$', userdel_data),
    url(r'^useredit_data/$', useredit_data),
    url(r'^useredit_commit/$', useredit_commit),
    #登录
    #url(r'^login/$', user_login, name='login'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^logout-then-login/$', logout_then_login, name='logout-then-login'),
    url(r'^$', dashboard, name='dashboard'),
    url(r'^password-change/$', password_change, name='password_change'),
    url(r'^password-change/done/$', password_change_done, name='password_change_done'),
    url(r'^password-reset/$', password_reset, name='password_reset'),
    url(r'^password-reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', password_reset_complete, name='password_reset_complete'),
    #用户注册
    url(r'^register/$', register, name='register'),
]

