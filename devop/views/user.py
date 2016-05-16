#!/usr/bin/python
# coding = utf-8

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,RequestContext

from devop.views.permission import PermissionVerify, SelfPaginator

@login_required
@PermissionVerify()
def ListUser(request):
    mList = User.objects.all()
    lst = SelfPaginator(request, mList, 20)
    kwvars = {
        'lpage':lst,
        'request':request,
    }
    return render_to_response('UserManage/user.list.html', kwvars)