#!/usr/bin/python
# coding = utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, RequestContext
from django.contrib.auth.decorators import login_required
from devop.views.permission import PermissionVerify, SelfPaginator
from .gitlab import all_projects, user_all_projects
from opman.forms import GitSettingForm, TokenForm
from opman.models import GitSetting, GitToken


@login_required
@PermissionVerify()
def Setting(request):
    cSetting = GitSetting.objects.all()
    if len(cSetting) == 0:
        form = GitSettingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('gitsettingurl'))
        else:
            form = GitSettingForm()
        kwvars = {
            'form': form,
            'request': request,
        }
        return render_to_response('GitLab/setting.add.html', kwvars, RequestContext(request))
    else:
        iGitSetting = GitSetting.objects.get(id=1)
        form = GitSettingForm(request.POST, instance=iGitSetting)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('gitsettingurl'))
        else:
            form = GitSettingForm(instance=iGitSetting)
        kwvars = {
            'form': form,
            'request': request,
        }
        return render_to_response('GitLab/setting.add.html', kwvars, RequestContext(request))


@login_required
@PermissionVerify()
def AddToken(request):
    form = TokenForm(request.POST)
    if form.is_valid():
        i = GitToken()
        form.save(commit=False)
        usertoken = form.cleaned_data['usertoken']
        i.usertoken=usertoken
        i.fullname = request.user.id
        i.save()
        return HttpResponseRedirect(reverse('listallprojectsurl'))
    else:
        form = TokenForm()
    kwvars = {
        'form': form,
        'request': request,
    }
    return render_to_response('GitLab/token.add.html', kwvars, RequestContext(request))


@login_required
@PermissionVerify()
def ListProjects(request):
    cUser = request.user
    cGitSetting = GitSetting.objects.get(id=1)
    host = cGitSetting.hostname
    rootoken = cGitSetting.rootoken
    path = '/api/v3/'
    if cUser.is_superuser:
        KList = all_projects(host, path, rootoken)
        lst = SelfPaginator(request, KList, 20)
    else:
        fullnameid = cUser.id
        try:
            usertoken = GitToken.objects.get(fullname_id=fullnameid)
        except Exception as e:
            print(e)
            return HttpResponseRedirect(reverse('tokenaddurl'))
        else:
            usertoken = GitToken.objects.get(fullname_id=fullnameid).usertoken
            KList = user_all_projects(host, path, usertoken)
            lst = SelfPaginator(request, KList, 20)

    kwvars = {
        'lpage': lst,
        'request': request,
    }
    return render_to_response('GitLab/projects.list.html', kwvars)



