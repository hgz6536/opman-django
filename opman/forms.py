from django import forms
from django.contrib.auth.models import User
from opman.models import PermissonList, RoleList

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