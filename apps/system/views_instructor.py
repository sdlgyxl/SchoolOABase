import re
import json
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.db.models import Q
from .mixin import LoginRequiredMixin
from .forms import InstructorCreateForm, InstructorUpdateForm, PasswordChangeForm
from base.models import Department

Instructor = get_user_model()
User = get_user_model()


class InstructorView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('system.view_instructor',)

    def get(self, request):
        '''
        if request.user.has_perm("system.view_instructor"):
            print('has perm view_instructor')
        else:
            print('no perm change_password')
        if request.user.has_perm("system.change_password"):
            print('has perm change_password')
        else:
            print('no perm view_instructor')
        '''
        return render(request, 'system/instructors/instructor.html')


class InstructorListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('system.view_instructor',)

    def get(self, request):
        fields = ['id', 'name', 'gender', 'mobile', 'email', 'department__name', 'post', 'superior__name', 'is_active']
        filters = dict()
        if 'select' in request.GET and request.GET['select']:
            filters['is_active'] = request.GET['select']
        res = dict(data=list(Instructor.objects.filter(**filters).values(*fields)))
        return HttpResponse(json.dumps(res), content_type='application/json')


class InstructorCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    添加用户
    """
    permission_required = ('system.add_instructor',)

    def get(self, request):
        instructors = Instructor.objects.exclude(username='admin')
        departments = Department.objects.values()
        groups = Group.objects.values()

        res = {
            'instructors': instructors,
            'departments': departments,
            'groups': groups,
        }
        return render(request, 'system/instructors/instructor-create.html', res)

    def post(self, request):
        instructor_create_form = InstructorCreateForm(request.POST)
        if instructor_create_form.is_valid():
            new_instructor = instructor_create_form.save(commit=False)
            new_instructor.password = make_password(instructor_create_form.cleaned_data['password'])
            new_instructor.save()
            instructor_create_form.save_m2m()
            res = {'status': 'success'}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(instructor_create_form.errors)
            error_messages = re.findall(pattern, errors)
            res = {
                'status': 'fail',
                'error_messages': error_messages[0]
            }
        return HttpResponse(json.dumps(res), content_type='application/json')


class InstructorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('system.change_instructor',)

    def get(self, request):
        instructor = get_object_or_404(Instructor, pk=int(request.GET['id']))
        instructors = Instructor.objects.exclude(Q(id=int(request.GET['id'])) | Q(username='admin'))
        departments = Department.objects.values()
        groups = Group.objects.values()
        instructor_groups = instructor.groups.values()
        res = {
            'instructor': instructor,
            'departments': departments,
            'instructors': instructors,
            'groups': groups,
            'instructor_groups': instructor_groups,
        }
        return render(request, 'system/instructors/instructor-update.html', res)

    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            instructor = get_object_or_404(Instructor, pk=int(request.POST['id']))
        else:
            instructor = get_object_or_404(Instructor, pk=int(request.user.id))
        instructor_update_form = InstructorUpdateForm(request.POST, instance=instructor)
        if instructor_update_form.is_valid():
            instructor_update_form.save()
            res = {"status": "success"}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(instructor_update_form.errors)
            error_messages = re.findall(pattern, errors)
            res = {
                'status': 'fail',
                'error_messages': error_messages[0]
            }
        return HttpResponse(json.dumps(res), content_type="application/json")


class PasswordChangeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('system.change_password',)

    def get(self, request):
        res = dict()
        if 'id' in request.GET and request.GET['id']:
            instructor = get_object_or_404(Instructor, pk=int(request.GET.get('id')))
            res['instructor'] = instructor
        return render(request, 'system/instructors/passwd_change.html', res)

    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            instructor = get_object_or_404(Instructor, pk=int(request.POST['id']))
            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                new_password = request.POST['password']
                instructor.set_password(new_password)
                instructor.save()
                res = {'status': 'success'}
            else:
                pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
                errors = str(form.errors)
                error_messages = re.findall(pattern, errors)
                res = {
                    'status': 'fail',
                    'error_messages': error_messages[0]
                }
            return HttpResponse(json.dumps(res), content_type='application/json')


class InstructorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    删除数据：支持删除单条记录和批量删除
    """
    permission_required = ('system.delete_instructor',)

    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST['id'].split(','))
            Instructor.objects.filter(id__in=id_list).delete()
            res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


class InstructorEnableView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    启用用户：单个或批量启用
    """
    permission_required = ('system.enable_user',)

    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            id_nums = request.POST.get('id')
            queryset = Instructor.objects.extra(where=["id IN(" + id_nums + ")"])
            queryset.filter(is_active=False).update(is_active=True)
            res = {'result': 'True'}
        return HttpResponse(json.dumps(res), content_type='application/json')


class InstructorDisableView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    启用用户：单个或批量启用
    """
    permission_required = ('system.disable_user',)

    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            id_nums = request.POST.get('id')
            queryset = Instructor.objects.extra(where=["id IN(" + id_nums + ")"])
            queryset.filter(is_active=True).update(is_active=False)
            res = {'result': 'True'}
        return HttpResponse(json.dumps(res), content_type='application/json')
