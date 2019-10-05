# -*- coding: utf-8 -*-
"""
@File    : views_permission.py
@Time    : 2019-08-28 8:06
@Author  : 杨小林
"""
import json
from django.views.generic import View
from django.shortcuts import HttpResponse, render, get_object_or_404
from .mixin import LoginRequiredMixin
from django.contrib.auth.models import Permission, ContentType
from . import forms


class PermissionView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, "system/permissions/permission.html")


class PermissionListView(LoginRequiredMixin, View):

    def get(self, request):
        fields = ['id', 'name', 'content_type__model', 'codename']
        filters = dict()
        if 'select' in request.GET and request.GET['select']:
            filters['name'] = request.GET['select']
        res = dict(data=list(
        Permission.objects.exclude(name__startswith='Can').filter(**filters).order_by('content_type').values(*fields)))
        return HttpResponse(json.dumps(res), content_type='application/json')


class PermissionEditView(LoginRequiredMixin, View):

    def get(self, request):
        res = dict(content_types=ContentType.objects.filter(id__gt=5))
        if 'id' in request.GET and request.GET['id']:
            permission = get_object_or_404(Permission, pk=request.GET['id'])
            res['permission'] = permission
        print(res['content_types'])
        return render(request, 'system/permissions/permission-edit.html', res)

    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            permission = get_object_or_404(Permission, pk=request.POST['id'])
        else:
            permission = Permission()
        permission_form = forms.PermissionForm(request.POST, instance=permission)
        if permission_form.is_valid():
            permission_form.save()
            res['result'] = True
        else:
            print(permission_form.errors)

        return HttpResponse(json.dumps(res), content_type='application/json')


class PermissionDeleteView(LoginRequiredMixin, View):
    """
    删除数据：支持删除单条记录和批量删除
    """

    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST['id'].split(','))
            Permission.objects.filter(id__in=id_list).delete()
            res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')
