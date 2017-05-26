import re

from django import forms

from operation.models import UserWant

class UserWantForm(forms.ModelForm):

    class Meta:
        model = UserWant
        fields = ["name", "phone_num", "course_name"]
    # 验证手机号码是否合法
    def clean_phone_num(self):
        phone_num = self.cleaned_data['phone_num']
        REGEX_PHONE_NUM = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_PHONE_NUM)
        if p.match(phone_num):
            return phone_num
        else:
            raise forms.ValidationError("手机号码不合法", code = "mobile_invalid")