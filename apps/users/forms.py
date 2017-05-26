from django import forms

from captcha.fields import CaptchaField

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField()


class ForgetPwdForm(forms.Form):
        email = forms.EmailField(required=True)
        captcha = CaptchaField()


# 忘记密码的时候重置密码，没有登录状态，不用验旧密码，但是需要用邮箱验证身份
class ResetPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)


# 用于处理文件的上传
class UploadImageForm(forms.ModelForm):
    class Meta:
        # 指定model
        model = UserProfile
        # 指定想要修改的字段
        fields = ['image']

# # 登录之后修改密码，需要验证就得密码，验证通过以后才能继续修改新的密码
# class ChangePasswpordForm(forms.Form):
#     oldpassword = forms.CharField(required=True, min_length=6)
#     password1 = forms.CharField(required=True, min_length=6)
#     password2 = forms.CharField(required=True, min_length=6)


# 用户登陆之后修改密码，但是暂时不用验证原来的密码
class UpdatePasswpordForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)


class UserChangeInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nickname','birthday','gender','address','phone_num']