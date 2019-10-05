import re
from django import forms
from django.contrib.auth import get_user_model
from . import models
from django.contrib.auth.models import Permission, Group
from django.db.models import ImageField

Instructor = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={"requeired": "请填写用户名"})
    password = forms.CharField(required=True, error_messages={"requeired": "请填写密码"})


class InstructorCreateForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": "密码不能为空",
            "min_length": "密码长度最少6位数",
        }
    )

    confirm_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": "确认密码不能为空",
            "min_length": "密码长度最少6位数",
        }
    )

    class Meta:
        model = Instructor
        fields = [
            'name', 'gender', 'birthday', 'username', 'mobile', 'email',
            'department', 'post', 'superior', 'is_active', 'password', 'groups', 'is_manager'
        ]

        error_messages = {
            "name": {"required": "姓名不能为空"},
            "username": {"required": "用户名不能为空"},
            "email": {"required": "邮箱不能为空"},
            "mobile": {
                "required": "手机号码不能为空",
                "max_length": "输入有效的手机号码",
                "min_length": "输入有效的手机号码"
            }
        }

    def clean(self):
        cleaned_data = super(InstructorCreateForm, self).clean()
        username = cleaned_data.get("username")
        mobile = cleaned_data.get("mobile", "")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if Instructor.objects.filter(username=username).count():
            raise forms.ValidationError('用户名：{}已存在'.format(username))

        if password != confirm_password:
            raise forms.ValidationError("两次密码输入不一致")

        if Instructor.objects.filter(mobile=mobile).count():
            raise forms.ValidationError('手机号码：{}已存在'.format(mobile))

        REGEX_MOBILE = "^1[3578]\d{9}$|^147\d{8}$|^176\d{8}$"
        if not re.match(REGEX_MOBILE, mobile):
            raise forms.ValidationError("手机号码非法")

        if Instructor.objects.filter(email=email).count():
            raise forms.ValidationError('邮箱：{}已存在'.format(email))


class InstructorProfileForm(forms.ModelForm):
    headimage = ImageField(upload_to='images/instructor/headimage',
                           default='images/default.jpg', max_length=100,
                           null=True, blank=True, verbose_name='头像')

    class Meta:
        model = Instructor
        fields = ['birthday', 'mobile', 'email', 'gender', 'headimage']


class InstructorUpdateForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = [
            'name', 'gender', 'birthday', 'username', 'mobile', 'email',
            'department', 'post', 'superior', 'is_active', 'groups', 'is_manager'
        ]

        error_messages = {
            "name": {"required": "姓名不能为空"},
            "username": {"required": "用户名不能为空"},
            "email": {"required": "邮箱不能为空"},
            "mobile": {
                "required": "手机号码不能为空",
                "max_length": "输入有效的手机号码",
                "min_length": "输入有效的手机号码"
            }
        }


class PasswordChangeForm(forms.Form):
    password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": u"密码不能为空"
        })

    confirm_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": u"确认密码不能为空"
        })

    def clean(self):
        cleaned_data = super(PasswordChangeForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("两次密码输入不一致")


class LoginPwdChangeForm(forms.Form):
    old_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": u"原密码不能为空"
        })

    new_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": u"新密码不能为空"
        })

    confirm_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": u"确认密码不能为空"
        })

    def clean(self):
        cleaned_data = super(LoginPwdChangeForm, self).clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            raise forms.ValidationError("两次密码输入不一致")


class PrivatePwdChangeForm(forms.Form):
    login_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": u"原密码不能为空"
        })

    new_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": u"新密码不能为空"
        })

    confirm_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": u"确认密码不能为空"
        })

    def clean(self):
        cleaned_data = super(PrivatePwdChangeForm, self).clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            raise forms.ValidationError("两次密码输入不一致")

class MenuForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = ['name', 'icon', 'parent', 'url', 'number']


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['name', 'content_type', 'codename']


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
