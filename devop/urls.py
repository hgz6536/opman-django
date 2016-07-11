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
from opman.views import dashboard, register
from django.contrib import admin
from django.contrib.auth.views import login, logout, logout_then_login, password_change, password_change_done, \
    password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from devop.views.permission import *
from devop.views.role import *
from devop.views.user import ListUser, EditUser, AddUser, DeleteUser
from devop.views.idc import ListIdc, AddIdc, EditIdc, DeleIdc
from devop.views.hosts import ListHost, AddHost, DeleHost, EditHost
from devop.views.attend import UploadXlsx, WriteData, DeleteXlsx, ListData, searchdata
from devop.views.gitman import Setting, ListProjects, AddToken
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
    url(r'^user/add/$', AddUser, name='adduserurl'),
    url(r'^user/edit/(?P<ID>\d+)/$', EditUser, name='edituserurl'),
    url(r'^user/delete/(?P<ID>\d+)/$', DeleteUser, name='deleteuserurl'),

    # 用户组管理
    url(r'^role/add/$', AddRole, name='addroleurl'),
    url(r'^role/list/$', ListRole, name='listroleurl'),
    url(r'^role/edit/(?P<ID>\d+)/$', EditRole, name='editroleurl'),
    url(r'^role/delete/(?P<ID>\d+)/$', DeleteRole, name='deleteroleurl'),

    # 密码管理
    url(r'^password-change/$', password_change, name='password_change'),
    url(r'^password-change/done/$', password_change_done, name='password_change_done'),
    url(r'^password-reset/$', password_reset, name='password_reset'),
    url(r'^password-reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$', password_reset_complete, name='password_reset_complete'),

    # 权限控制
    url(r'^permission/deny/$', Nopermisson, name='permissiondenyurl'),
    url(r'^permission/add/$', AddPermission, name='addpermissonurl'),
    url(r'^permission/list/$', ListPermission, name='listpermissionurl'),
    url(r'^permission/edit/(?P<ID>\d+)/$', EditPermission, name='editpermissionurl'),
    url(r'^permission/delete/(?P<ID>\d+)/$', DelePermission, name='deletepermissionurl'),

    # IDC机房信息管理
    url(r'^idc/list/$', ListIdc, name='listidcurl'),
    url(r'^idc/add/$', AddIdc, name='addidcurl'),
    url(r'^idc/delete/(?P<ID>\d+)/$', DeleIdc, name='deleteidcurl'),
    url(r'^idc/edit/(?P<ID>\d+)/$', EditIdc, name='editidcurl'),

    # 主机管理
    url(r'^host/list/$', ListHost, name='listhosturl'),
    url(r'^host/add/$', AddHost, name='addhosturl'),
    url(r'^host/delete/(?P<ID>\d+)/$', DeleHost, name='deletehosturl'),
    url(r'^host/edit/(?P<ID>\d+)/$', EditHost, name='edithosturl'),

    # 考勤管理
    url(r'^upload/xlsx/$', UploadXlsx, name='uploadxlsxurl'),
    url(r'^write/data/(?P<ID>\d+)/$', WriteData, name='writedataurl'),
    url(r'^delete/xlsx/(?P<ID>\d+)/$', DeleteXlsx, name='delxlsxurl'),
    url(r'^list/data/$', ListData, name='listdataurl'),
    url(r'^seach/data/$', searchdata, name='searchdataurl'),

    #Git管理
    url(r'^git/setting/$', Setting, name='gitsettingurl'),
    url(r'^list/all/projects/$', ListProjects, name='listallprojectsurl'),
url(r'^add/token/$', AddToken, name='tokenaddurl'),
]
