# -*-coding:UTF-8 -*-
import random
from devop.utils import base
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib import auth
from opman.models import Project_Config, Project_Order, Assets, Log_Assets, Cron_Config, Ansible_Playbook,Global_Config,Email_Config


@login_required(login_url='/login')
def index(request):
    userlist = Project_Order.objects.raw('''SELECT id,order_user FROM opman_project_order GROUP BY order_user;''')
    userlist = [u.orde_user for u in userlist]
    datelist = [base.getDaysAgo(num) for num in range(0, 7)][::-1]
    datalist = []
    for user in userlist:
        valuelist = []
        data = {}
        for startTime in datelist:
            sql = """SELECT id,IFNULL(count(0),0) as count from opman_project_order WHERE 
                    date_format(create_time,"%%Y%%m%%d") = {startTime} and order_user='{user}'""".format(
                startTime=startTime, user=user)
            userData = Project_Order.objects.raw(sql)
            if userData[0].count == 0:
                valuelist.append(random.randint(1, 10))
            else:
                valuelist.append(userData[0].count)
            data[user] = valuelist
            datalist.append(data)
    orderNotice = Project_Order.objects.all().order_by('-id')[0:10]
    monthList = [base.getDaysAgo(num)[0:6] for num in (0, 30, 60, 90, 120, 150, 180)][::-1]
    monthDataList = []
    for ms in monthList:
        startTime = int(ms + '01')
        endTime = int(ms + '31')
        data = {}
        data['date'] = ms
        for user in userlist:
            sql = """SELECT id,IFNULL(count(0),0) as count from opsmanage_project_order WHERE date_format(create_time,"%%Y%%m%%d") >= {startTime} and 
                                    date_format(create_time,"%%Y%%m%%d") <= {endTime} and order_user='{user}'""".format(
                    startTime=startTime, endTime=endTime, user=user)
            userData = Project_Order.objects.raw(sql)
            if userData[0].count == 0:
                data[user] = random.randint(1, 100)
            else:
                data[user] = userData[0].count
        monthDataList.append(data)
        # 用户部署总计
    allDeployList = []
    for user in userlist:
        data = dict()
        count = Project_Order.objects.filter(order_user=user).count()
        data['user'] = user
        data['count'] = count
        allDeployList.append(data)
        # 获取资产更新日志
    assetsLog = Log_Assets.objects.all().order_by('-id')[0:10]
    # 获取所有项目数据
    assets = Assets.objects.all().count()
    project = Project_Config.objects.all().count()
    cron = Cron_Config.objects.all().count()
    playbook = Ansible_Playbook.objects.all().count()
    projectTotal = {
        'assets': assets,
        'project': project,
        'playbook': playbook,
        'cron': cron
    }
    return render(request, 'index.html', {"user": request.user, "orderList": datalist,
                                                  "userList": userlist, "dateList": datelist,
                                                  "monthDataList": monthDataList, "monthList": monthList,
                                                  "allDeployList": allDeployList, "assetsLog": assetsLog,
                                                  "orderNotice": orderNotice, "projectTotal": projectTotal})


def login(request):
    if request.session.get('username') is not None:
        return HttpResponseRedirect('/', {"user": request.user})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            request.session['username'] = username
            return HttpResponseRedirect('/user/center/', {"user": request.user})
        else:
            if request.method == "POST":
                return render(request, 'login.html', {"login_error_info": "用户名不错存在，或者密码错误！"})
            else:
                return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')

def noperm(request):
    return render(request,'noperm.html', {"user": request.user})


@login_required(login_url='/login')
def config(request):
    if request.method == "GET":
        try:
            config = Global_Config.objects.get(id=1)
        except:
            config = None
        try:
            email = Email_Config.objects.get(id=1)
        except:
            email = None
        return render(request,'config.html', {"user": request.user, "config": config,"email": email})
    elif request.method == "POST":
        if request.POST.get('op') == "log":
            try:
                count = Global_Config.objects.filter(id=1).count()
            except:
                count = 0
            if count > 0:
                Global_Config.objects.filter(id=1).update(
                    ansible_model=request.POST.get('ansible_model'),
                    ansible_playbook=request.POST.get('ansible_playbook'),
                    cron=request.POST.get('cron'),
                    project=request.POST.get('project'),
                    assets=request.POST.get('assets', 0),
                    server=request.POST.get('server', 0),
                    email=request.POST.get('email', 0),
                )
            else:
                config = Global_Config.objects.create(
                    ansible_model=request.POST.get('ansible_model'),
                    ansible_playbook=request.POST.get('ansible_playbook'),
                    cron=request.POST.get('cron'),
                    project=request.POST.get('project'),
                    assets=request.POST.get('assets'),
                    server=request.POST.get('server'),
                    email=request.POST.get('email')
                )
            return JsonResponse({'msg': '配置修改成功', "code": 200, 'data': []})
        elif request.POST.get('op') == "email":
            try:
                count = Email_Config.objects.filter(id=1).count()
            except:
                count = 0
            if count > 0:
                Email_Config.objects.filter(id=1).update(
                    site=request.POST.get('site'),
                    host=request.POST.get('host', None),
                    port=request.POST.get('port', None),
                    user=request.POST.get('user', None),
                    passwd=request.POST.get('passwd', None),
                    subject=request.POST.get('subject', None),
                    cc_user=request.POST.get('cc_user', None),
                )
            else:
                Email_Config.objects.create(
                    site=request.POST.get('site'),
                    host=request.POST.get('host', None),
                    port=request.POST.get('port', None),
                    user=request.POST.get('user', None),
                    passwd=request.POST.get('passwd', None),
                    subject=request.POST.get('subject', None),
                    cc_user=request.POST.get('cc_user', None),
                )
            return JsonResponse({'msg': '配置修改成功', "code": 200, 'data': []})
