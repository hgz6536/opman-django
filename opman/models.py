# coding:utf-8
from django.db import models


# Create your models here.
class HostList(models.Model):
    idcinfo = models.CharField(max_length=100, verbose_name=u'机房')
    ipinfo = models.GenericIPAddressField()
    repairinfo = models.BigIntegerField()
    brandinfo = models.CharField(max_length=15, verbose_name=u'品牌')
    buytime = models.TimeField()
    hostname = models.CharField(max_length=50, verbose_name=u'主机名')
    osinfo = models.CharField(max_length=50, verbose_name=u'系统版本')
    modelinfo = models.CharField(max_length=50, verbose_name=u'型号')
    memoryinfo = models.CharField(max_length=15, verbose_name=u'内存信息')
    diskinfo = models.CharField(max_length=50, verbose_name=u'硬盘信息')
    cpuinfo = models.CharField(max_length=50, verbose_name=u'CPU信息')
    snnum = models.BigIntegerField()
    usefor = models.CharField(max_length=80, verbose_name=u'用途')

class RepairInfo(models.Model):
    ipaddr = models.GenericIPAddressField()
    starttime = models.TimeField()
    badinfo = models.CharField(max_length=100, verbose_name=u'损坏信息')
    repairmethod = models.CharField(max_length=100, verbose_name=u'维修方案')
    endtime = models.TimeField()
    costifno = models.CharField(max_length=50, verbose_name=u'维修费用')
'''
class HostGroup(models.Model):
    groupname = models.CharField(max_length=20, verbose_name=u'组名')
'''


class AppList(models.Model):
    ipaddr = models.GenericIPAddressField()
    appname = models.CharField(max_length=15, verbose_name=u'应用名字')


class IdcList(models.Model):
    idcname = models.CharField(max_length=20, verbose_name=u'合作商')
    cityname = models.CharField(max_length=5, verbose_name=u'所在城市')
    position = models.CharField(max_length=20, verbose_name=u'地理位置')
    hostnum = models.IntegerField()
    bandwidth = models.IntegerField()
    expense = models.IntegerField()
    starttime = models.DateField(auto_now_add=False, verbose_name=u'开始时间')
    iphonecall = models.CharField(max_length=20, verbose_name=u'值班电话')
    status = models.BooleanField()
'''
    def __unicode__(self):
        return self.idcname
'''