# -*- coding: utf-8 -*-
"""
@File    : views_department.py
@Time    : 2019-08-27 13:09
@Author  : 杨小林
"""
import json
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.generic.base import View, TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from .models import Department
from system.mixin import LoginRequiredMixin
from . import forms
from django.contrib.auth import get_user_model

Instructor = get_user_model()


class DepartmentView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'base/departments/department.html')


class DepartmentListView(LoginRequiredMixin, View):
    def get(self, request):
        fields = ['id', 'name', 'description', 'parent__name']
        filters = dict()
        if 'select' in request.GET and request.GET['select']:
            filters['name'] = request.GET['select']
        res = dict(data=list(Department.objects.filter(**filters).values(*fields)))
        return HttpResponse(json.dumps(res), content_type='application/json')


class DepartmentEditView(LoginRequiredMixin, View):

    def get(self, request):
        res = dict(department_all=Department.objects.all())
        if 'id' in request.GET and request.GET['id']:
            department = get_object_or_404(Department, pk=request.GET['id'])
            res['department'] = department
        return render(request, 'base/departments/department-edit.html', res)

    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            department = get_object_or_404(Department, pk=request.POST['id'])
        else:
            department = Department()
        department_form = forms.DepartmentForm(request.POST, instance=department)
        if department_form.is_valid():
            department_form.save()
            res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


class DepartmentDeleteView(LoginRequiredMixin, View):
    """
    删除数据：支持删除单条记录和批量删除
    """

    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST['id'].split(','))
            Department.objects.filter(id__in=id_list).delete()
            res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


class Department2InstructorView(LoginRequiredMixin, View):
    """
    部门分配用户
    """

    def get(self, request):
        if 'id' in request.GET and request.GET['id']:
            department = get_object_or_404(Department, pk=int(request.GET['id']))
            added_instructors = department.instructor_set.all()
            all_instructors = Instructor.objects.all()
            un_add_instructors = set(all_instructors).difference(added_instructors)
            res = dict(department=department, added_instructors=added_instructors,
                       un_add_instructors=list(un_add_instructors))
        return render(request, 'base/departments/department-instructor.html', res)

    def post(self, request):
        res = dict(result=False)
        id_list = None
        department = get_object_or_404(Department, pk=int(request.POST['id']))
        if 'selInstructors' in request.POST and request.POST.getlist('selInstructors', []):
            id_list = map(int, request.POST.getlist('selInstructors', []))
        department.instructor_set.clear()
        if id_list:
            for instructor in Instructor.objects.filter(id__in=id_list):
                department.instructor_set.add(instructor)
        res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')
