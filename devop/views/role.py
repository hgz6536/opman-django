# from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from devop.views.permission import PermissionVerify, SelfPaginator
from opman.forms import RoleListForm
from opman.models import RoleList


@login_required
@PermissionVerify()
def ListRole(request):
    rList = RoleList.objects.all()
    lst = SelfPaginator(request, rList, 20)
    kwvars = {
        'lpage': lst,
        'request': request,
    }
    return render_to_response('UserManage/role.list.html', kwvars, RequestContext(request))


@login_required
@PermissionVerify()
def AddRole(request):
    if request.method == "POST":
        form = RoleListForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listroleurl'))
    else:
        form = RoleListForm()
    kwvars = {
        'form': form,
        'request': request,
    }
    return render_to_response('UserManage/role.add.html', kwvars, RequestContext(request))


@login_required
@PermissionVerify()
def EditRole(request, ID):
    iRole = RoleList.objects.get(id=ID)
    if request.method == "POST":
        form = RoleListForm(request.POST, instance=iRole)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listroleurl'))
    else:
        form = RoleListForm(instance=iRole)
    kwvars = {
        'ID': ID,
        'form': form,
        'request': request,
    }
    return render_to_response('UserManage/role.edit.html', kwvars, RequestContext(request))


@login_required
@PermissionVerify()
def DeleteRole(request, ID):
    RoleList.objects.filter(id=ID).delete()
    return HttpResponseRedirect(reverse('listroleurl'))
