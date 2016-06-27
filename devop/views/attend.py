#!/usr/bin/python
# coding = utf-8
from opman.forms import XlsxUpload
from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext
from django.contrib.auth.decorators import login_required
from devop.views.permission import PermissionVerify, SelfPaginator
from opman.models import Xlsx

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

    return render_to_response('attend/upload.html', {'uf': uf}, RequestContext(request))
