# -*- coding: utf-8 -*-
"""
@File    : views_leave.py
@Time    : 2019-09-06 14:48
@Author  : 杨小林
"""
from django.views.generic import TemplateView, View
from django.utils.timezone import now
from tools.funcs import get_prev_month
from system.mixin import LoginRequiredMixin
from .views_mixin import AttendanceListView, AttendanceApplyView, AttendanceDeleteView, AttendanceProcessView
from .models import Vacation, VacationLog
from base.models import Department
from django.contrib.auth import get_user_model
from .forms import LeaveApplyForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404

User = get_user_model()


class VacationView(LoginRequiredMixin, View):
    # template_name = 'attendance/vacations/index.html'

    def get(self, request):
        user = request.user
        filters = {}
        vacations = Vacation.objects.filter(**filters)
        if user.has_perm('view_all_Vacation'):
            pass
        elif user.has_perm('view_deprtment_Vacation'):
            vacations = vacations.filter(instructor__department__id=user.department.id)
        else:
            vacations = vacations.filter(instructor_id=user.id)
        departments = Department.objects.all().values(*['id', 'name'])
        users = User.objects.filter(is_Active=True).values(*['id', 'name'])
        res = dict(vacations=vacations, departments=departments, users=users)
        return render(request, 'attendance/vacations/index.html', res)


class VacationLogView(LoginRequiredMixin, View):
    def get(self, request):
        if 'id' in request.POST and request.POST['id']:
            id = int(request.POST['id'])
            user = request.user
            vacation = get_object_or_404(Vacation, instructor_id=id)
            vacationlogs = VacationLog.objects.filter(instructor_id=id).order_by('-id').values()
            res = dict(vacation=vacation, vacationlogs=vacationlogs)
            return render(request, 'attendance/vacations/vacation-detail.html', res)


class VacationCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    添加
    """
    permission_required = ('attendance.add_leave',)

    def get(self, request):
        return render(request, 'attendance/vacations/vacation-detail.html', res)

    def post(self, request):
        return render(request, 'attendance/vacations/vacation-detail.html', res)
