# coding:utf-8
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

'''
IDC 管理模块的表格
'''

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

'''
用户管理模块的表格

class User(models.Model):
    mail = models.CharField(max_length=20, default='null', verbose_name=u'用户邮箱')
    username = models.CharField(max_length=20, default='null', verbose_name=u'用户名字')
    pwd = models.CharField(max_length=20, verbose_name=u'用户密码')
    groupnum = models.SmallIntegerField(default= 0)
'''
class UserGroup(models.Model):
    groupname = models.CharField(max_length=10,default='null', verbose_name=u'分组名字')
    groupnum = models.SmallIntegerField(default=0)

'''
权限相关
'''
class PermissonList(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=255)
    username = models.CharField(max_length=30, default=None)
    groupname = models.CharField(max_length=80, default=None)

    def __unicode__(self):
        return '%s(%s)' %(self.name, self.url)

class RoleList(models.Model):
    name = models.CharField(max_length=64)
    permission = models.ManyToManyField(PermissonList, null = True, blank= True)

    def __unicode__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError(u'邮件地址必填')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using = self.db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True, db_index=True)
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    nickname = models.CharField(max_length=64, null=True)
    sex = models.CharField(max_length=2, null=True)
    role = models.ForeignKey(RoleList, null=True, blank=True)

    object = UserManager()
    UERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True