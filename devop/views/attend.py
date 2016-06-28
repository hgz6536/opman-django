#!/usr/bin/python
# coding = utf-8
from opman.forms import XlsxUpload
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from django.contrib.auth.decorators import login_required
from devop.views.permission import PermissionVerify, SelfPaginator
from opman.models import Xlsx, KaoQin
from opman.models import MyUser as User
from .analystor import getalldate, gethours, getworktime
from datetime import datetime, timedelta
from openpyxl import load_workbook


@login_required
@PermissionVerify()
def ListData(request):
    KList = KaoQin.objects.all()
    lst = SelfPaginator(request, KList, 20)
    kwvars = {
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
            return HttpResponse('upload ok!')
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
        if u == '':
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
    Xlsx.objects.filter(id=ID).delete()
    return HttpResponseRedirect(reverse('uploadxlsxurl'))
