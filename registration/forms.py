# -*- coding: utf-8 -*-
import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class LoginForm(AuthenticationForm):

    username = forms.RegexField(label=_(u"用户名"),regex=r'^\w+$', widget=forms.TextInput(
        attrs={'maxlength': 30, 'class': 'input width220', 'placeholder': _("Username")}))
    password = forms.CharField(label=_(u"密码"),widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'input width220', 'placeholder': _("Password")}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        if self.errors:
            for f_name in self.fields:
                classes = self.fields[f_name].widget.attrs.get('class', '')
                classes += ' has-error'
                self.fields[f_name].widget.attrs['class'] = classes
    """def clean(self):
        try:
            user = User.objects.get(
                username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_(u"用户或密码错误，请重新登录！"))"""

class RegistrationForm(forms.Form):

    username = forms.RegexField(regex=r'^\w+$', label=_(u"用户名"),widget=forms.TextInput(
        attrs={'maxlength': 30, 'class': 'input width220', 'placeholder': _("登录时的用户名")}))
    mobile = forms.CharField(label=_(u"手机号"),required=False,widget=forms.TextInput(
        attrs={'maxlength': 60, 'class': 'input width220', 'placeholder': _("请输入手机号")}))
    email = forms.EmailField(label=_(u"您的邮箱"),widget=forms.TextInput(
        attrs={'maxlength': 60, 'class': 'input width220', 'placeholder': _("找回账户重要邮箱，请确保能够使用")}))
    qq= forms.CharField(label=_(u"QQ"),required=False,widget=forms.TextInput(
        attrs={'maxlength': 60, 'class': 'input width220', 'placeholder': _("ＱＱ")}))
    password1 = forms.CharField(label=_(u"登录密码"),widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'input width220', 'placeholder': _("请输入6到16位的任意字符作为密码")}))
    password2 = forms.CharField(label=_(u"确认密码"),widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'input width220', 'placeholder': _("请再输一次密码")}))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        if self.errors:
            for f_name in self.fields:
                if f_name in self.errors:
                    classes = self.fields[f_name].widget.attrs.get('class', '')
                    classes += ' has-error'
                    self.fields[f_name].widget.attrs['class'] = classes

    def clean_username(self):
        try:
            user = User.objects.get(
                username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_(u"用户已注册,请换个用户名注册！"))

    def clean_mobile(self):
        try:
            if 'mobile' in self.clean_data:
                self.cleaned_data['mobile']
        except :
            return self.cleaned_data['mobile']
        raise forms.ValidationError(_(u"请输入手机号码！"))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u"两次密码不相同，请重新输入！"))
        return self.cleaned_data
