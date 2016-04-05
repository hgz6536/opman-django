# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from opman.models import IdcList
# Create your views here.
# from django.http import request


def index(req):
    return render_to_response('index.html')


def idcinfo(req):
    """

    :param req:
    :return: idc list
    """
    idc_list = IdcList.objects.all()
    return render_to_response('idc_info.html',{'idc_list':idc_list})


def idcadd_play(req):
    return render_to_response('idc_add.html')


def idcadd_data(req):
    if 'idcname' and 'cityname' and 'position' and 'hostnum' and 'iphonecall' and 'status' in req.GET:
        idcname_new = req.GET['idcname']
        cityname_new = req.GET['cityname']
        position_new = req.GET['position']
        hostnum_new = req.GET['hostnum']
        bandwidth_new = req.GET['bandwidth']
        expense_new = req.GET['expense']
        starttime_new = req.GET['starttime']
        iphonecall_new = req.GET['iphonecall']
        sta = req.GET['status']
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
    idcname_now = i.idcname
    cityname_now = i.cityname
    position_now = i.position
    hostnum_now = i.hostnum
    bandwidth_now = i.bandwidth
    expense_now = i.expense
    starttime_now = str(i.starttime)
    iphonecall_now = i.iphonecall
    status_now = i.status
    return render_to_response('idc_edit.html', {'id': id_now,
                                               'idcname': idcname_now,
                                               'cityname': cityname_now,
                                               'position': position_now,
                                               'hostnum': hostnum_now,
                                               'bandwidth': bandwidth_now,
                                               'expense': expense_now,
                                               'starttime': starttime_now,
                                               'iphonecall': iphonecall_now,
                                               'status': status_now})


def idcedit_commit(req):
    id_now = req.GET['id']
    #print(id_now)
    idcname_now = req.GET['idcname']
    cityname_now = req.GET['cityname']
    position_now = req.GET['position']
    hostnum_now = req.GET['hostnum']
    bandwidth_now = req.GET['bandwidth']
    expense_now = req.GET['expense']
    starttime_now = req.GET['starttime']
    iphonecall_now = req.GET['iphonecall']
    sta = req.GET['status']
    if sta == 'OK':
        status_now = 1
    else:
        status_now = 0

    try:
        i = IdcList(id=id_now)
        i.idcname = idcname_now
        i.cityname = cityname_now
        i.position = position_now
        i.hostnum = hostnum_now
        i.bandwidth = bandwidth_now
        i.expense = expense_now
        i.starttime = starttime_now
        i.iphonecall = iphonecall_now
        i.status = status_now
        i.save()
        return HttpResponseRedirect('/idc/')
    except Exception as e:
        return HttpResponse(e)