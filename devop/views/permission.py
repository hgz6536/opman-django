#!/usr/bin/env python
# coding = uft-8

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from django.contrib.auth.decorators import login_required

from opman.forms import PermissionListForm
from opman.models import RoleList, PermissonList
from django.contrib.auth.models import Group
from opman.models import MyUser as User
from opman.views import SelfPaginator


def PermissionVerify():
    '''
    权限认证模块;
     此模块先判断用户是不是管理员（is_superuser为True）,如果是管理，则有全部权限，如果不是则获取request.user和request.path,
     判断2个参数是不是匹配，匹配则有权限，反之则无
    '''

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            iUser = User.objects.get(username=request.user)
            iGroup = Group.objects.filter(user=request.user)
            # uid = iUser.id
            glst = []
            for g in iGroup.all():
                glst.append(str(g))
            if not iUser.is_superuser:
                if 'sa' not in glst:
                    if not PermissonList.objects.filter(username=iUser.username):
                        return HttpResponseRedirect(reverse('permissiondenyurl'))
                    else:
                        role_permisson = PermissonList.objects.filter(username=request.user)
                        role_permisson = role_permisson.all()
                        matchurl = []
                        for x in role_permisson:
                            if request.path == x.url or request.path.rstrip('/') == x.url:
                                matchurl.append(x.url)
                            elif request.path.startswith(x.url):
                                matchurl.append(x.url)
                            else:
                                pass
                        print('%s---->matchUrl:%s' % (request.user, str(matchurl)))
                        if len(matchurl) == 0:
                            return HttpResponseRedirect(reverse('permissiondenyurl'))
                else:
                    pass
            else:
                pass
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


@login_required
def Nopermisson(request):
    kwvars = {
        'request': request,
    }
    return render_to_response('UserManage/permission.no.html', kwvars)


@login_required
@PermissionVerify()
def AddPermission(request):
    form = PermissionListForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('listpermissionurl'))
    else:
        form = PermissionListForm()
    kwvars = {
        'form': form,
        'request': request,
    }
    return render_to_response('UserManage/permission.add.html', kwvars, RequestContext(request))


@login_required
@PermissionVerify()
def ListPermission(request):
    mList = PermissonList.objects.all()
    lst = SelfPaginator(request, mList, 20)
    kwvars = {
        'lpage': lst,
        'request': request,
    }
    return render_to_response('UserManage/permission.list.html', kwvars)


@login_required
@PermissionVerify()
def EditPermission(request, ID):
    iPermission = PermissonList.objects.get(id=ID)
    if request.method == "POST":
        form = PermissionListForm(request.POST, instance=iPermission)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("listpermissionurl"))
    else:
        form = PermissionListForm(instance=iPermission)
    kwvars = {
        'ID': ID,
        'form': form,
        'request': request,
    }
    return render_to_response('UserManage/permission.edit.html', kwvars, RequestContext(request))


@login_required
@PermissionVerify()
def DelePermission(request, ID):
    PermissonList.objects.filter(id=ID).delete()
    return HttpResponseRedirect(reverse('listpermissionurl'))
