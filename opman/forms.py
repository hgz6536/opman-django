from django import forms
from opman.models import MyUser as User
from opman.models import PermissonList, RoleList
from opman.models import IdcList, HostList


class XlsxUpload(forms.Form):
    date = forms.DateField(label=u'日期', widget=forms.DateInput())
    filename = forms.FileField(label=u'文件上传')


# 用户登录,注册,编辑,权限
class LoginForm(forms.Form):
    username = forms.CharField(label=u'账号', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=u'重复密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    SEX_CHOICES = (
        ('男', '男'),
        ('女', '女'),
    )
    sex = forms.CharField(
        widget=forms.Select(choices=SEX_CHOICES, attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'birthday', 'email', 'sex', 'role', 'fullname')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['birthday'].label = u'生日'
        self.fields['email'].label = u'邮箱'
        self.fields['sex'].label = u'性别'

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(u'两次输入的密码不一样')
        return cd['password2']


class UserAddForm(forms.ModelForm):
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=u'重复密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    SEX_CHOICES = (
        ('男', '男'),
        ('女', '女'),
    )
    sex = forms.CharField(
        widget=forms.Select(choices=SEX_CHOICES, attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'birthday', 'email', 'sex', 'role', 'permission', 'fullname')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control'}),
            'permission': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '10', 'multiple': 'multiple'}),
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserAddForm, self).__init__(*args, **kwargs)
        self.fields['birthday'].label = u'生日'
        self.fields['email'].label = u'邮箱'
        self.fields['sex'].label = u'性别'
        self.fields['permission'].label = u'权限'

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(u'两次输入的密码不一样')
        return cd['password2']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_active', 'permission', 'fullname')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.Select(choices=((True, u'启用'), (False, u'禁用')), attrs={'class': 'form-control'}),
            'permission': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '10', 'multiple': 'multiple'}),
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['permission'].label = u'权限'


class PermissionListForm(forms.ModelForm):
    class Meta:
        model = PermissonList
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(PermissionListForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = u'名 称'
        self.fields['name'].error_messages = {'required': u'请输入名称'}
        self.fields['url'].label = u'URL'
        self.fields['url'].error_messages = {'required': u'请输入URL'}


# 用户组
class RoleListForm(forms.ModelForm):
    class Meta:
        model = RoleList
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'permission': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '10', 'multiple': 'multiple'}),
        }

    def __init__(self, *args, **kwargs):
        super(RoleListForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = u'名称'
        self.fields['name'].error_messages = {'required': u'请输入名称'}
        self.fields['permission'].label = u'权限'
        self.fields['permission'].required = False


# IDC
class IdcListForm(forms.ModelForm):
    STAS_CHOICES = (
        ('1', 'OK'),
        ('0', 'NO'),
    )
    status = forms.IntegerField(
        widget=forms.Select(choices=STAS_CHOICES)
    )

    class Meta:
        model = IdcList
        fields = '__all__'
        widgets = {
            'idcname': forms.TextInput(attrs={'class': 'form-control'}),
            'cityname': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'hostnum': forms.TextInput(attrs={'class': 'form-control'}),
            'bandwidth': forms.TextInput(attrs={'class': 'form-control'}),
            'expense': forms.TextInput(attrs={'class': 'form-control'}),
            'starttime': forms.DateInput(attrs={'class': 'form-control'}),
            'iphonecall': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(IdcListForm, self).__init__(*args, **kwargs)
        self.fields['idcname'].label = u'公司名称'
        self.fields['idcname'].error_messages = {'required': u'请输入名称'}
        self.fields['cityname'].label = u'机房城市'
        self.fields['cityname'].error_messages = {'required': u'请输入城市名字'}
        self.fields['position'].label = u'机房地址'
        self.fields['position'].error_messages = {'required': u'请输入机房地址'}
        self.fields['hostnum'].label = u'主机数量'
        self.fields['hostnum'].error_messages = {'required': u'主机数量'}
        self.fields['bandwidth'].label = u'机房带宽(M)'
        self.fields['bandwidth'].error_messages = {'required': u'请输入带宽'}
        self.fields['expense'].label = u'机房年费(元)'
        self.fields['expense'].error_messages = {'required': u'请输入年费'}
        self.fields['starttime'].label = u'开始合作'
        self.fields['starttime'].error_messages = {'required': u'请输入开始合作时间'}
        self.fields['iphonecall'].label = u'机房电话'
        self.fields['iphonecall'].error_messages = {'required': u'请输入机房电话'}
        self.fields['status'].label = u'使用状态'


# 主机

class HostListForm(forms.ModelForm):
    STAS_CHOICES = (
        ('1', u'启用中'),
        ('0', u'未使用'),
    )
    REPAIR_CHOICES = (
        ('1', u'正常'),
        ('0', u'故障'),
    )
    status = forms.IntegerField(
        widget=forms.Select(choices=STAS_CHOICES)
    )
    repairinfo = forms.IntegerField(
        widget=forms.Select(choices=REPAIR_CHOICES)
    )

    class Meta:
        model = HostList
        fields = '__all__'
        widgets = {
            'idcinfo': forms.TextInput(attrs={'class': 'form-control'}),
            'ipinfo': forms.TextInput(attrs={'class': 'form-control'}),
            # 'repairinfo': forms.TextInput(attrs={'class':'form-control'}),
            'brandinfo': forms.TextInput(attrs={'class': 'form-control'}),
            'buytime': forms.TextInput(attrs={'class': 'form-control'}),
            'hostname': forms.TextInput(attrs={'class': 'form-control'}),
            'osinfo': forms.TextInput(attrs={'class': 'form-control'}),
            'modelinfo': forms.TextInput(attrs={'class': 'form-control'}),
            'memoryinfo': forms.TextInput(attrs={'class': 'form-control'}),
            'diskinfo': forms.TextInput(attrs={'class': 'form-control'}),
            'cpuinfo': forms.TextInput(attrs={'class': 'form-control'}),
            'snnum': forms.TextInput(attrs={'class': 'form-control'}),
            'usefor': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(HostListForm, self).__init__(*args, **kwargs)
        '''
        for field in self.fields.values():
            field.error_messages = {'required':'*'}

        self.fields['idcinfo'].label= u'所在机房'
        self.fields['idcinfo'].error_messages = {'required':u'请输入机房名称'}
        self.fields['ipinfo'].label = u'主机ip'
        self.fields['ipinfo'].error_messages = {'required':u'请输入主机ip'}
        self.fields['repairinfo'].label = u'维修信息'
        self.fields['repairinfo'].error_messages = {'required': u'请输入维修信息'}
        self.fields['brandinfo'].label = u'主机品牌'
        self.fields['brandinfo'].error_messages = {'required': u'主机品牌'}
        self.fields['buytime'].label= u'购买时间'
        self.fields['buytime'].error_messages = {'required':u'请输入购买时间'}
        self.fields['hostname'].label = u'主机名字'
        self.fields['hostname'].error_messages = {'required':u'请输入主机名字'}
        self.fields['osinfo'].label = u'主机系统'
        self.fields['osinfo'].error_messages = {'required': u'请输入主机系统'}
        self.fields['modelinfo'].label = u'主机类型'
        self.fields['modelinfo'].error_messages = {'required': u'请输入主机类型'}
        self.fields['memoryinfo'].label = u'内存大小'
        self.fields['memoryinfo'].error_messages = {'required': u'请输入内存大小'}
        self.fields['diskinfo'].label = u'硬盘大小'
        self.fields['diskinfo'].error_messages = {'required': u'请输入硬盘大小'}
        self.fields['cpuinfo'].label = u'CPU型号'
        self.fields['cpuinfo'].error_messages = {'required': u'请输入CPU 型号'}
        self.fields['snnum'].label = u'售后代码'
        self.fields['snnum'].error_messages = {'required': u'请输入售后代码'}
        self.fields['usefor'].label = u'主机用途'
        self.fields['usefor'].error_messages = {'required': u'请输入主机用途'}
        '''
        self.fields['repairinfo'].label = u'维修信息'
        self.fields['status'].label = u'使用状态'
