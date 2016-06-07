#!/usr/bin/python
# coding = utf-8

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponseRedirect
from opman.models import HostList
from devop.views.permission import PermissionVerify, SelfPaginator
from opman.forms import HostListForm


@login_required
@PermissionVerify()
def ListHost(request):
    mList = HostList.objects.all()
    lst = SelfPaginator(request, mList, 20)
    kwvars = {
        'lpage': lst,
        'request': request,
    }
    return render_to_response('HostManage/host.list.html', kwvars)


@login_required
@PermissionVerify()
def AddHost(request):
    form = HostListForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('listhosturl'))
    else:
        form = HostListForm()

    kwvars = {
        'form': form,
        'request': request,
    }

    return render_to_response('HostManage/host.add.html', kwvars, RequestContext(request))


@login_required
@PermissionVerify()
def EditHost(request, ID):
    host = HostList.objects.get(id=ID)

    if request.method == 'POST':
        form = HostListForm(request.POST, instance=host)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listhosturl'))
    else:
        form = HostListForm(instance=host)

    kwvars = {
        'ID': ID,
        'form': form,
        'request': request,
    }

    return render_to_response('HostManage/host.edit.html', kwvars, RequestContext(request))


@login_required
@PermissionVerify()
def DeleHost(request, ID):
    HostList.objects.filter(id=ID).delete()
    return HttpResponseRedirect(reverse('listhosturl'))
