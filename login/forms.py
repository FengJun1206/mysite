from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    username = forms.CharField(
        label='用户名',                # 在表单里表现为 label 标签
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control'})   # 添加 css 属性
    )

    password = forms.CharField(
        label='密码',
        max_length=256,
        # 该字段在form表单里表现为<input type='password' />，也就是密码输入框。
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    captcha = CaptchaField(
        label='验证码',
        required=True,
        error_messages={
            'required': '验证码不能为空'
        }
    )


class RegisterForm(forms.Form):
    """注册"""
    username = forms.CharField(
        max_length=128,
        label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        max_length=256,
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    password2 = forms.CharField(
        max_length=256,
        label='确认密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    email = forms.CharField(
        max_length=128,
        label='邮箱地址',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    sex = forms.ChoiceField(
        label='性别',
        choices=gender
    )

    captcha = CaptchaField(label='验证码')



