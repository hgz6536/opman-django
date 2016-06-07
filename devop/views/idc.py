#!/usr/bin/python
# coding = utf-8

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponseRedirect
from opman.models import IdcList
from devop.views.permission import PermissionVerify, SelfPaginator
from opman.forms import IdcListForm


@login_required
@PermissionVerify()
def ListIdc(request):
    mList = IdcList.objects.all()
    lst = SelfPaginator(request, mList, 20)
    kwvars = {
        'lpage': lst,
        'request': request,
    }
    return render_to_response('IdcManage/idc.list.html', kwvars)


@login_required
@PermissionVerify()
def AddIdc(request):
    form = IdcListForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('listidcurl'))
    else:
        form = IdcListForm()

    kwvars = {
        'form': form,
        'request': request,
    }

    return render_to_response('IdcManage/idc.add.html', kwvars, RequestContext(request))


@login_required
@PermissionVerify()
def EditIdc(request, ID):
    idc = IdcList.objects.get(id=ID)

    if request.method == 'POST':
        form = IdcListForm(request.POST, instance=idc)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listidcurl'))
    else:
        form = IdcListForm(instance=idc)

    kwvars = {
        'ID': ID,
        'form': form,
        'request': request,
    }

    return render_to_response('IdcManage/idc.edit.html', kwvars, RequestContext(request))


@login_required
@PermissionVerify()
def DeleIdc(request, ID):
    IdcList.objects.filter(id=ID).delete()
    return HttpResponseRedirect(reverse('listidcurl'))
