#!/usr/bin/python
# coding = utf-8
from opman.forms import XlsxUpload
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from django.contrib.auth.decorators import login_required
from devop.views.permission import PermissionVerify, SelfPaginator
from opman.models import Xlsx, KaoQin
from opman.models import MyUser as User
from .analystor import getalldate, gethours, getworktime
from datetime import datetime, timedelta
from openpyxl import load_workbook
import os

@login_required
@PermissionVerify()
def ListData(request):
    cUser = request.user
    fullname = cUser.id
    if cUser.is_superuser or cUser.role.name == '人事行政':
        KList = KaoQin.objects.all()
        nameinput = 'able'
    else:
        KList = KaoQin.objects.filter(fullname_id=fullname)
        nameinput = 'disabled'
    lst = SelfPaginator(request, KList, 31)
    kwvars = {
        'nameinput': nameinput,
        'lpage': lst,
        'request': request,
    }
    return render_to_response('attend/data.list.html', kwvars)


@login_required
@PermissionVerify()
def UploadXlsx(request):
    if request.method == "POST":
        uf = XlsxUpload(request.POST, request.FILES)
        if uf.is_valid():
            date = uf.cleaned_data['date']
            filename = uf.cleaned_data['filename']
            xlsx = Xlsx()
            xlsx.date = date
            xlsx.filename = filename
            xlsx.save()
            return HttpResponseRedirect(reverse('uploadxlsxurl'))
    else:
        uf = XlsxUpload()
    xlist = Xlsx.objects.all()
    lst = SelfPaginator(request, xlist, 20)
    kwvars = {
        'uf': uf,
        'lpage': lst,
        'request': request,
    }
    return render_to_response('attend/upload.html', kwvars, RequestContext(request))


@login_required
@PermissionVerify()
def WriteData(request, ID):
    xlsx = Xlsx.objects.get(id=ID)
    filename = xlsx.filename
    date = xlsx.date
    wb = load_workbook(filename=filename)
    ws = wb.get_sheet_by_name('Sheet 1')
    rows = ws.rows
    alldata = []
    for row in rows:
        line = [col.value for col in row]
        alldata.append(line)
    year = int(date.strftime('%Y'))
    month = int(date.strftime('%m'))
    datelist = getalldate(year, month)
    user = User.objects.all()
    userlist = []
    for i in user:
        userlist.append(i.fullname)
    for u in userlist:
        if u == '' or u is None:
            pass
        else:
            for day in datelist:
                nextday = datetime.strptime(
                    day, '%Y-%m-%d').date() + timedelta(days=1)
                jilu = getworktime(u, day, alldata)
                jilu1 = getworktime(u, nextday, alldata)
                a = gethours(u, day, jilu1, jilu)
                if a == None:
                    pass
                else:
                    fullname = a['username']
                    uid = user.get(fullname=fullname).id
                    kq = KaoQin()
                    kq.date = a['date']
                    kq.week = a['myweek']
                    kq.on = a['on']
                    kq.off = a['off']
                    kq.plus = a['plus']
                    kq.late = a['late']
                    kq.leave = a['leave']
                    kq.content = a['content']
                    kq.fullname_id = uid
                    kq.save()
    return HttpResponseRedirect(reverse('listdataurl'))


@login_required
@PermissionVerify()
def DeleteXlsx(request, ID):
    xlsx = Xlsx.objects.get(id=ID)
    file = xlsx.filename
    mydate = xlsx.date
    year = int(mydate.strftime('%Y'))
    month = int(mydate.strftime('%m'))
    KaoQin.objects.filter(date__month=month).delete()
    Xlsx.objects.filter(id=ID).delete()
    os.remove(str(file))
    return HttpResponseRedirect(reverse('uploadxlsxurl'))


@login_required
@PermissionVerify()
def searchdata(request):
    cUser = request.user
    cid = cUser.id
    user = User.objects.all()
    start = request.GET["start"]
    end = request.GET["end"]
    if cUser.is_superuser or cUser.role.name == '人事行政':
        nameinput = 'able'
        fullname = request.GET["username"]
        id = user.get(fullname=fullname).id
        if not fullname:
            KList = KaoQin.objects.filter(date__range=[start, end])
        if not start and not end:
            KList = KaoQin.objects.filter(fullname_id=id)
        if start and end:
            KList = KaoQin.objects.filter(fullname_id=id).filter(date__range=[start, end])
        if not fullname and not start and not end:
            pass
    else:
        nameinput = 'disabled'
        if not start or not end:
            pass
        if start and end:
            KList = KaoQin.objects.filter(fullname_id = cid).filter(date__range=[start, end])
    lst = SelfPaginator(request, KList, 31)
    kwvars = {
        'nameinput': nameinput,
        'lpage': lst,
        'request': request,
    }
    return render_to_response('attend/data.list.html', kwvars, RequestContext(request))
