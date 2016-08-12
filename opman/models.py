# coding:utf-8
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser

# Create your models here.

'''
IDC 管理模块的表格
'''


class HostList(models.Model):
    idcinfo = models.CharField(max_length=100, verbose_name=u'机房')
    ipinfo = models.GenericIPAddressField(verbose_name=u'主机IP')
    repairinfo = models.IntegerField(verbose_name=u'维修状态')
    brandinfo = models.CharField(max_length=15, verbose_name=u'品牌')
    buytime = models.DateField(verbose_name=u'购买日期')
    hostname = models.CharField(max_length=50, verbose_name=u'主机名')
    osinfo = models.CharField(max_length=50, verbose_name=u'系统版本')
    modelinfo = models.CharField(max_length=50, verbose_name=u'型号')
    memoryinfo = models.CharField(max_length=15, verbose_name=u'内存信息')
    diskinfo = models.CharField(max_length=50, verbose_name=u'硬盘信息')
    cpuinfo = models.CharField(max_length=50, verbose_name=u'CPU信息')
    snnum = models.CharField(max_length=30, verbose_name=u'服务编号')
    usefor = models.CharField(max_length=80, verbose_name=u'用途')
    status = models.IntegerField(default=None, verbose_name=u'是否在用')


class RepairInfo(models.Model):
    ipaddr = models.GenericIPAddressField()
    starttime = models.TimeField()
    badinfo = models.CharField(max_length=100, verbose_name=u'损坏信息')
    repairmethod = models.CharField(max_length=100, verbose_name=u'维修方案')
    endtime = models.TimeField()
    costifno = models.CharField(max_length=50, verbose_name=u'维修费用')


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

    def __str__(self):
        return self.idcname


'''
权限相关
'''


class PermissonList(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'权限名称')
    url = models.CharField(max_length=255, verbose_name=u'URL地址')

    def __str__(self):
        return '%s(%s)' % (self.name, self.url)


class RoleList(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'部门名称')
    permission = models.ManyToManyField(PermissonList, blank=True, verbose_name=u'权限')

    def __str__(self):
        return self.name


class MyUser(AbstractUser):
    fullname = models.CharField(max_length=64, null=True, unique=True, default=None, verbose_name=u'姓名')
    birthday = models.DateField(null=True, blank=True, default=None, verbose_name=u'生日')
    sex = models.CharField(max_length=2, null=True, verbose_name=u'性别')
    role = models.ForeignKey(RoleList, null=True, blank=True, verbose_name=u'部门')
    permission = models.ManyToManyField(PermissonList, blank=True, verbose_name=u'权限')


'''
考勤相关
'''


class KaoQin(models.Model):
    fullname = models.ForeignKey(MyUser, null=False, blank=False, verbose_name=u'姓名')
    date = models.DateField(default=None, null=False, blank=False, verbose_name=u'日期')
    week = models.CharField(default=None, max_length=10, verbose_name=u'星期')
    on = models.DateTimeField(null=True, blank=True, verbose_name=u'上班时间')
    off = models.DateTimeField(null=True, blank=True, verbose_name=u'下班时间')
    plus = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=u'加班时间')
    late = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=u'迟到时间')
    leave = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=u'请假时间')
    content = models.CharField(max_length=100, null=True, verbose_name=u'情况分析')


class Xlsx(models.Model):
    date = models.DateField(null=False, blank=False, verbose_name=u'日期')
    filename = models.FileField(upload_to='./upload/xlsx/', verbose_name=u'选择文件')

    def __str__(self):
        return self.filename


'''
Git相关
'''


class GitSetting(models.Model):
    hostname = models.CharField(max_length=100, null=True, unique=True, default=None, verbose_name=u'GitLab域名')
    rootoken = models.CharField(max_length=30, null=True, unique=True, default=None, verbose_name=u'管理员token')
    sourcepath = models.CharField(max_length=50, null=True, unique=True, default=None, verbose_name=u'上线源目录')
    ngxpath = models.CharField(max_length=50, null=True, unique=True, default=None, verbose_name=u'nginx目录')
    testserver = models.GenericIPAddressField(default='127.0.0.1', verbose_name=u'测试服务器IP')
    devserver = models.GenericIPAddressField(default='127.0.0.1', verbose_name=u'开发服务器IP')
    ngxconf = models.TextField(verbose_name='Ngx配置文件', default=None)


class ProjectSetting(models.Model):
    url = models.URLField(null=False, unique=True, verbose_name=u'项目URL')
    devpath = models.CharField(max_length=50, null=True, unique=True, default=None, verbose_name=u'开发目录')
    testpath = models.CharField(max_length=50, null=True, unique=True, default=None, verbose_name=u'测试目录')
    testhostname = models.CharField(max_length=50, null=True, unique=True, default=None, verbose_name=u'测试域名')
    devhostname = models.CharField(max_length=50, null=True, unique=True, default=None, verbose_name=u'开发域名')
    ngxtestconf = models.TextField(verbose_name='Ngx测试', default=None)
    ngxdevtconf = models.TextField(verbose_name='Ngx开发', default=None)


class ProjectApply(models.Model):
    title = models.CharField(max_length=30, null=False, default=None, verbose_name=u'上线名称')
    projectname = models.CharField(max_length=30, null=False, default=None, verbose_name=u'项目名称')
    projectid = models.IntegerField(null=False, default=None, verbose_name=u'项目ID')
    projecturl = models.CharField(max_length=100, null=False, default=None, verbose_name=u'项目URL')
    projectbranch = models.CharField(max_length=30, null=False, default=None, verbose_name=u'项目分支')
    commitid = models.CharField(max_length=10, null=False, default=None, verbose_name=u'上线版本号')
    applytime = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0, verbose_name=u'当前状态')


class GitToken(models.Model):
    usertoken = models.CharField(max_length=30, null=True, unique=True, default=None, verbose_name=u'用户token')
    fullname = models.ForeignKey(MyUser, null=False, blank=False, verbose_name=u'姓名')
