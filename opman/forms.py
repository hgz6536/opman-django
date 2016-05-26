from django import forms
from django.contrib.auth.models import User
from opman.models import PermissonList, RoleList
from opman.models import IdcList

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label=u'重复密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(u'两次输入的密码不一样')
        return cd['password2']

class PermissionListForm(forms.ModelForm):
    class Meta:
        model = PermissonList
        fields = '__all__'
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'url' : forms.TextInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'groupname': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(PermissionListForm, self).__init__(*args, **kwargs)
        self.fields['name'].label= u'名 称'
        self.fields['name'].error_messages = {'required':u'请输入名称'}
        self.fields['url'].label = u'URL'
        self.fields['url'].error_messages = {'required':u'请输入URL'}
        self.fields['username'].label = u'用户名'
        self.fields['username'].error_messages = {'required': u'请输入用户名'}
        self.fields['groupname'].label = u'组名'
        self.fields['groupname'].error_messages = {'required': u'请输入组名'}

class RoleListForm(forms.ModelForm):
    class Meta:
        model=RoleList
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'permission':forms.SelectMultiple(attrs={'class':'form-control','size':'10','multiple':'multiple'}),
        }

    def __init__(self, *args, ** kwargs):
        super(RoleListForm, self).__init__(*args, **kwargs)
        self.fields['name'].label=u'名称'
        self.fields['name'].error_messages={'required':u'请输入名称'}
        self.fields['permission'].label=u'URL'
        self.fields['permission'].required=False

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email', 'is_active', 'first_name', 'last_name')
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control'}),
            #'password': forms.HiddenInput,
            'email' : forms.TextInput(attrs={'class':'form-control'}),
            'is_active' : forms.Select(choices=((True, u'启用'),(False, u'禁用')),attrs={'class':'form-control'}),
        }

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
            'idcname': forms.TextInput(attrs={'class':'form-control'}),
            'cityname': forms.TextInput(attrs={'class':'form-control'}),
            'position': forms.TextInput(attrs={'class':'form-control'}),
            'hostnum': forms.TextInput(attrs={'class': 'form-control'}),
            'bandwidth': forms.TextInput(attrs={'class': 'form-control'}),
            'expense': forms.TextInput(attrs={'class': 'form-control'}),
            'starttime': forms.DateInput(attrs={'class': 'form-control'}),
            'iphonecall': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(IdcListForm, self).__init__(*args, **kwargs)
        self.fields['idcname'].label= u'公司名称'
        self.fields['idcname'].error_messages = {'required':u'请输入名称'}
        self.fields['cityname'].label = u'机房城市'
        self.fields['cityname'].error_messages = {'required':u'请输入城市名字'}
        self.fields['position'].label = u'机房地址'
        self.fields['position'].error_messages = {'required': u'请输入机房地址'}
        self.fields['hostnum'].label = u'主机数量'
        self.fields['hostnum'].error_messages = {'required': u'主机数量'}
        self.fields['bandwidth'].label= u'机房带宽(M)'
        self.fields['bandwidth'].error_messages = {'required':u'请输入带宽'}
        self.fields['expense'].label = u'机房年费(元)'
        self.fields['expense'].error_messages = {'required':u'请输入年费'}
        self.fields['starttime'].label = u'开始合作'
        self.fields['starttime'].error_messages = {'required': u'请输入开始合作时间'}
        self.fields['iphonecall'].label = u'机房电话'
        self.fields['iphonecall'].error_messages = {'required': u'请输入机房电话'}
        self.fields['status'].label = u'使用状态'
