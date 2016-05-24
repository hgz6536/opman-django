from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from devop.views.permission import PermissionVerify, SelfPaginator
from opman.forms import RoleListForm

@login_required
@PermissionVerify()
def ListGroup(request):
    gList = Group.objects.all()
    lst = SelfPaginator(request, gList, 20)


    kwvars = {
        'lpage': lst,
        'request': request,
    }
    return render_to_response('UserManage/group.list.html', kwvars, RequestContext(request))


@login_required
@PermissionVerify()
def AddGroup(request):
    if request.method == "POST":
        form = RoleListForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listroleurl'))
    else:
        form = RoleListForm()

    kwvars = {
        'form':form,
        'request':request,
    }

    return render_to_response('UserManage/group.add.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def EditGroup(request,ID):
    iRole = Group.objects.get(id=ID)

    if request.method == "POST":
        form = RoleListForm(request.POST,instance=iRole)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listroleurl'))
    else:
        form = RoleListForm(instance=iRole)

    kwvars = {
        'ID':ID,
        'form':form,
        'request':request,
    }

    return render_to_response('UserManage/group.edit.html',kwvars,RequestContext(request))