# _*_ encoding:utf-8 _*_

from django import forms
from operation.models import UserAsk
import re

class UserAskFoem(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name']

    #必须clean开头
    def clean_mobile(self):
        """验证手机号是否合法"""
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码异常")