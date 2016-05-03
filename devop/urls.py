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
from opman.views import index, idcinfo, idcadd_play, idcadd_data, idcdel_data, idcedit_commit, idcedit_data, userinfo, useradd_play, useradd_data, useredit_data, useredit_commit

# from django.contrib import admin

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
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
    url(r'^useredit_data/$', useredit_data),
    url(r'^useredit_commit/$', useredit_commit),
]
