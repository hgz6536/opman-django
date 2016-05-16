# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect

from opman.models import IdcList, User, UserGroup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
# Create your views here.
# from django.http import request
def SelfPaginator(request, List, Limit):
    paginator = Paginator(List, int(Limit))
    page = request.GET.get('page')
    try:
        lst = paginator.page(page)
    except PageNotAnInteger:
        lst = paginator.page(1)
    except EmptyPage:
        lst = paginator.page(paginator.num_pages)
    return lst
#首页
def index(req):
    return render_to_response('index.html')

#IDC 模块
@csrf_protect
@login_required
def idcinfo(request):
    idc_list = IdcList.objects.all()
    return render_to_response('idc_info.html',{'idc_list':idc_list})


def idcadd_play(req):
    return render_to_response('idc_add.html')


def idcadd_data(req):
    req_get_key = ['iphonecall', 'bandwidth', 'expense', 'hostnum', 'position', 'status', 'cityname', 'idcname', 'starttime']
    if 'idcname' and 'cityname' and 'position' and 'hostnum' and 'iphonecall' and 'status' in req.GET:
        data_list = []
        for k in req_get_key:
            data_list.append(req.GET[k])

        iphonecall_new, bandwidth_new, expense_new, hostnum_new, position_new, sta, cityname_new, idcname_new, starttime_new = data_list
        if sta == 'OK':
            status_new = 1
        else:
            status_new = 0

        try:
            i = IdcList(idcname=idcname_new, cityname=cityname_new, position=position_new, hostnum=hostnum_new, bandwidth=bandwidth_new, expense=expense_new, starttime=starttime_new, iphonecall=iphonecall_new, status=status_new)
            i.save()
            return HttpResponseRedirect('/idc/')
        except Exception as e:
            print(e)
            return HttpResponse(e)
    else:
        return HttpResponse('有必填项未完成')


def idcdel_data(req):
    id_now = req.GET['id']
    try:
        i = IdcList.objects.get(id=id_now)
        i.delete()
        return HttpResponseRedirect('/idc/')
    except Exception as e:
        return HttpResponse(e)


def idcedit_data(req):
    id_now = req.GET['id']
    i = IdcList.objects.get(id=id_now)
    return render_to_response('idc_edit.html', {'id': id_now, 'idcname': i.idcname, 'cityname': i.cityname, 'position': i.position, 'hostnum': i.hostnum, 'bandwidth': i.bandwidth, 'expense': i.expense, 'starttime': i.starttime, 'iphonecall': i.iphonecall, 'status': i.status})


def idcedit_commit(req):
    id_now = req.GET['id']
    #print(id_now)
    req_get_key = ['iphonecall', 'bandwidth', 'expense', 'hostnum', 'position', 'status', 'cityname', 'idcname', 'starttime']
    data_list = []
    for k in req_get_key:
        data_list.append(req.GET[k])
    iphonecall_now, bandwidth_now, expense_now, hostnum_now, position_now, sta, cityname_now, idcname_now, starttime_now = data_list
    if sta == 'OK':
        status_now = 1
    else:
        status_now = 0

    try:
        i = IdcList(id=id_now, idcname=idcname_now, cityname=cityname_now, position=position_now, hostnum=hostnum_now, bandwidth=bandwidth_now, expense=expense_now, starttime=starttime_now, iphonecall=iphonecall_now, status=status_now)
        i.save()
        return HttpResponseRedirect('/idc/')
    except Exception as e:
        return HttpResponse(e)

#用户模块
def userinfo(req):
    user_list = User.objects.all()
    return render_to_response('user_info.html',{'user_list':user_list})

def useradd_play(req):
    groupnum_list = []
    for i in UserGroup.objects.all():
        groupnum_list.append(i.groupnum)
    return render_to_response('user_add.html',{'groupnum_list':groupnum_list})

def useradd_data(req):
    req_get_key = ['username', 'mail', 'pw2', 'groupnum']
    if 'username' and 'mail' and 'pw1' and 'pw2' and 'groupnum' in req.GET:
        data_list = []
        for key in req_get_key:
            data_list.append(req.GET[key])
        username_new, mail_new, pw2_new, groupnum_new = data_list
        if groupnum_new == '运维':
            groupnum_new = 0
        else:
            groupnum_new = 1
        try:
            u = User(username=username_new, pwd=pw2_new, groupnum=groupnum_new, mail=mail_new)
            u.save()
            return HttpResponseRedirect('/user/')
        except Exception as e:
            print(e)
            return HttpResponse(e)

    else:
        return HttpResponse('有必填项未完成')

def userdel_data(req):
    id_now = req.GET['id']
    try:
        i = User.objects.get(id=id_now)
        i.delete()
        return HttpResponseRedirect('/user/')
    except Exception as e:
        return HttpResponse(e)

def useredit_data(req):
    id_now = req.GET['id']
    u = User.objects.get(id=id_now)
    return render_to_response('user_edit.html', {'id':id_now, 'username':u.username, 'mail':u.mail, 'pwd':u.pwd, 'groupnum':u.groupnum})

def useredit_commit(req):
    id_now = req.GET['id']
    req_get_key = ['username', 'mail', 'pw1', 'pw2', 'groupnum']
    data_list = []
    for key in req_get_key:
        data_list.append(req.GET[key])
    username_now, mail_now, pw1_now, pw2_now, groupnum_new = data_list
    if pw1_now == pw2_now:
        pass
    else:
        return HttpResponseServerError(u'500 Error,两次输入的密码不一样')
    if groupnum_new == '运维':
        groupnum_new = 0
    else:
        groupnum_new = 1
    try:
        u = User(id = id_now, username = username_now, mail = mail_now, pwd = pw2_now, groupnum = groupnum_new)
        u.save()
        return HttpResponseRedirect('/user/')
    except Exception as e:
        print(e)
        return HttpResponse(e)

'''
用户登录
'''
from .forms import LoginForm, UserRegistrationForm
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated' \
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form':form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section':'dashboard'})

