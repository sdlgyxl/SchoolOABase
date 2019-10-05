# -*- coding: utf-8 -*-
"""
@File    : views_group.py
@Time    : 2019-08-30 19:38
@Author  : 杨小林
"""

import json
from django.views.generic import View
from django.shortcuts import HttpResponse, render, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from .models import Menu
from .mixin import LoginRequiredMixin
from . import forms

Instructor = get_user_model()


# class GroupView(LoginRequiredMixin, PermissionRequiredMixin, View):
#    permission_required = ('system.查看角色',)
class GroupView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "system/groups/group.html")


# class GroupListView(LoginRequiredMixin, PermissionRequiredMixin, View):
#    permission_required = ('system.查看角色',)

class GroupListView(LoginRequiredMixin, View):
    def get(self, request):
        limit, start, page = 20, 1, 5
        if 'limit' in request.GET and request.GET['limit']:
            limit = int(request.GET['limit'])
        if 'start' in request.GET and request.GET['start']:
            start = int(request.GET['start'])
        if 'page' in request.GET and request.GET['page']:
            page = request.GET['page']

        fields = ['id', 'name']
        filters = dict()
        if 'select' in request.GET and request.GET['select']:
            filters['name__contains'] = request.GET['select']
        total = Group.objects.filter(**filters).count()
        groups = Group.objects.filter(**filters).order_by('-id')[start:start + limit].values(*fields)

        res = dict(data=list(groups))
        res['limit'] = limit
        res['page'] = page
        res['total'] = total
        return HttpResponse(json.dumps(res), content_type='application/json')


class GroupEditView(LoginRequiredMixin, View):
    # permission_required = ('system.增加角色', 'system.修改角色')

    def get(self, request):
        res = dict()
        if 'id' in request.GET and request.GET['id']:
            group = get_object_or_404(Group, pk=request.GET['id'])
            res['group'] = group
        return render(request, 'system/groups/group-edit.html', res)

    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            group = get_object_or_404(Group, pk=request.POST['id'])
        else:
            group = Group()
        group_form = forms.GroupForm(request.POST, instance=group)
        if group_form.is_valid():
            group_form.save()
            res['result'] = True
        else:
            print(group_form.errors)

        return HttpResponse(json.dumps(res), content_type='application/json')


class GroupDeleteView(LoginRequiredMixin, View):
    """
    删除数据：支持删除单条记录和批量删除
    """

    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST['id'].split(','))
            Group.objects.filter(id__in=id_list).delete()
            res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


class Group2InstructorView(LoginRequiredMixin, View):
    """
    角色关联用户
    """

    def get(self, request):
        if 'id' in request.GET and request.GET['id']:
            group = get_object_or_404(Group, pk=int(request.GET.get('id')))
            added_instructors = group.user_set.all()
            all_instructors = Instructor.objects.all()
            un_add_instructors = set(all_instructors).difference(added_instructors)
            res = dict(group=group, added_instructors=added_instructors, un_add_instructors=list(un_add_instructors))
        return render(request, 'system/groups/group2instructor.html', res)

    def post(self, request):
        res = dict(result=False)
        id_list = None
        group = get_object_or_404(Group, pk=int(request.POST.get('id')))
        if 'selInstructors' in request.POST and request.POST['selInstructors']:
            id_list = map(int, request.POST.getlist('selInstructors', []))
        group.user_set.clear()
        if id_list:
            for instructor in Instructor.objects.filter(id__in=id_list):
                group.user_set.add(instructor)
        res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


class Group2MenuView(LoginRequiredMixin, View):
    """
    角色绑定菜单
    """

    def get(self, request):
        if 'id' in request.GET and request.GET['id']:
            group = get_object_or_404(Group, pk=request.GET['id'])
            ret = dict(group=group)
            return render(request, 'system/groups/group2menu.html', ret)

    def post(self, request):
        res = dict(result=False)
        group = get_object_or_404(Group, pk=request.POST['id'])
        tree = json.loads(self.request.POST['tree'])
        group.menu_set.clear()
        for menu in tree:
            if menu['checked'] is True:
                menu_checked = get_object_or_404(Menu, pk=menu['id'])
                print(menu_checked.id, menu_checked)
                group.menu_set.add(menu_checked)
        res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


class Group2MenuListView(LoginRequiredMixin, View):
    """
    获取zTree菜单列表
    """

    def get(self, request):
        fields = ['id', 'name', 'parent']
        if 'id' in request.GET and request.GET['id']:
            group = Group.objects.get(id=request.GET.get('id'))
            group_menus = group.menu_set.values(*fields)
            ret = dict(data=list(group_menus))
        else:
            menus = Menu.objects.all()
            ret = dict(data=list(menus.values(*fields)))
        return HttpResponse(json.dumps(ret), content_type='application/json')


class Group2PermissionView(LoginRequiredMixin, View):
    """
    角色关联用户
    """

    def get(self, request):
        if 'id' in request.GET and request.GET['id']:
            group = get_object_or_404(Group, pk=int(request.GET.get('id')))
            added_permissions = group.permissions.all().order_by('content_type')
            all_permissions = Permission.objects.exclude(name__startswith='Can').order_by('content_type')
            un_add_permissions = set(all_permissions).difference(added_permissions)
            res = dict(group=group, added_permissions=added_permissions, un_add_permissions=list(un_add_permissions))
            return render(request, 'system/groups/group2permission.html', res)

    def post(self, request):
        res = dict(result=False)
        id_list = None
        group = get_object_or_404(Group, pk=int(request.POST.get('id')))
        print(request.POST)
        if 'selPermissions' in request.POST and request.POST['selPermissions']:
            id_list = map(int, request.POST.getlist('selPermissions', []))
            print(id_list)
        group.permissions.clear()
        if id_list:
            for permission in Permission.objects.filter(id__in=id_list):
                group.permissions.add(permission)
        res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')
