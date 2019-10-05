# -*- coding: utf-8 -*-
"""
@File    : views_home.py
@Time    : 2019-09-01 10:59
@Author  : 杨小林
"""
import re
import json
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model, authenticate
from django.views.generic.base import View
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from common.tools import datetime_verify
from .mixin import LoginRequiredMixin
from .forms import LoginPwdChangeForm, PrivatePwdChangeForm

Instructor = get_user_model()


class InstructorProfileView(LoginRequiredMixin, View):
    def get(self, request):
        res = dict(myself=get_object_or_404(Instructor, pk=int(request.user.id)))
        res['state'] = request.GET.get('state')
        return render(request, 'system/home/profile.html', res)

    def post(self, request):
        try:
            myself = Instructor.objects.filter(id=int(request.user.id))[0]
            if datetime_verify(request.POST.get('birthday')):
                myself.birthday = request.POST.get('birthday')
            myself.mobile = request.POST.get('mobile')
            myself.email = request.POST.get('email')
            myself.gender = request.POST.get('gender')
            if request.FILES.get('headimage'):
                myself.headimage = request.FILES.get('headimage')
            myself.save()
            return redirect('/system/home/profile/?state=success')
        except:
            return redirect('/system/home/profile/?state=fail')


class LoginPwdChangeView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'system/home/login_pwd_change.html')

    def post(self, request):
        myself = Instructor.objects.filter(id=request.user.id)[0]
        form = LoginPwdChangeForm(request.POST)
        res = dict(status='fail')
        if form.is_valid():
            old_password = request.POST['old_password']
            new_password = request.POST['new_password']
            user = authenticate(username=request.user.username, password=old_password)
            if user is not None:
                myself.set_password(new_password)
                myself.save()
                res = {'status': 'success'}
            else:
                res = {'status': 'fail', 'errors': '原密码不正确！'}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(form.errors)
            error_messages = re.findall(pattern, errors)
            res = {
                'status': 'fail',
                'error_messages': error_messages[0]
            }
        return HttpResponse(json.dumps(res), content_type='application/json')


class PrivatePwdChangeView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'system/home/private_pwd_change.html')

    def post(self, request):
        myself = Instructor.objects.filter(id=request.user.id)[0]
        form = PrivatePwdChangeForm(request.POST)
        res = dict(status='fail')
        if form.is_valid():
            login_password = request.POST['login_password']
            new_password = request.POST['new_password']
            user = authenticate(username=request.user.username, password=login_password)
            if user is not None:
                myself.private_password = make_password(new_password)
                myself.save()
                res = {'status': 'success'}
            else:
                res = {'status': 'fail', 'errors': '原密码不正确！'}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(form.errors)
            error_messages = re.findall(pattern, errors)
            res = {
                'status': 'fail',
                'error_messages': error_messages[0]
            }
        return HttpResponse(json.dumps(res), content_type='application/json')
