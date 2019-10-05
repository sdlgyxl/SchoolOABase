# -*- coding: utf-8 -*-
"""
@File    : views_leave.py
@Time    : 2019-09-06 14:48
@Author  : 杨小林
"""
from django.views.generic import TemplateView
from django.utils.timezone import now
from tools.funcs import get_prev_month
from system.mixin import LoginRequiredMixin
from .views_mixin import AttendanceListView, AttendanceApplyView, AttendanceDeleteView, AttendanceProcessView
from .models import Leave, leave_type_choice
from base.models import Department
from django.contrib.auth import get_user_model
from .forms import LeaveApplyForm
from django.contrib.auth.mixins import PermissionRequiredMixin

User = get_user_model()


class LeaveView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance/index.html'

    def get_context_data(self):
        self.kwargs['moduleName'] = '请假申请'
        query_month = now()
        months = []
        for i in range(0, 12):
            months.append(query_month.strftime('%Y-%m'))
            query_month = get_prev_month(query_month)[0]
        self.kwargs['months'] = months
        self.kwargs['departments'] = Department.objects.all().values(*['id', 'name'])
        self.kwargs['users'] = User.objects.filter(is_active=1).values(*['id', 'name'])
        self.kwargs['moduleUrl'] = 'leave'
        self.kwargs['not_agree_col'] = 9
        self.kwargs['columns'] = [{"title": "ID", "data": "id"},
                                  {"title": "申请人", "data": "applicant__name"},
                                  {"title": "开始时间", "data": "start_time"},
                                  {"title": "结束时间", "data": "end_time"},
                                  {"title": "请假类型", "data": "leave_type"},
                                  {"title": "请假时长", "data": "leave_hours"},
                                  {"title": "请假原因", "data": "reason"},
                                  {"title": "审批步骤", "data": "step"},
                                  {"title": "审批人", "data": "auditor__name"},
                                  {"title": "审批结果", "data": "result"}]
        return super().get_context_data(**self.kwargs)


class LeaveListView(AttendanceListView):
    model = Leave
    fields = ['id', 'applicant__name', 'start_time', 'end_time', "leave_type",
              "leave_hours", "reason", "step", "auditor__name", "result"]
    perm_all = 'attendance.view_all_leave'
    perm_department = 'attendance.view_deprtment_leave'
    key2values = ['step', 'result', 'leave_type']
    selects = [['month', 'start_time__startswith'], ['dept', 'applicant__department__id'], ['user', 'applicant__id']]

    def get(self, request):
        return super().get(request)


class LeaveApplyView(PermissionRequiredMixin, AttendanceApplyView):
    """
    添加
    """
    permission_required = ('attendance.add_leave',)
    moduleName = "leave"
    moduleTitle = "请假申请"
    form = LeaveApplyForm
    moduleId = 2
    res = dict(leave_type=leave_type_choice)

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)


class LeaveDeleteView(AttendanceDeleteView):
    model = Leave
    moduleId = 2

    def post(self, request):
        return super().post(request)


class LeaveProcessView(AttendanceProcessView):
    """
    审批
    """

    model = Leave
    moduleId = 2
    moduleName = "leave"
    moduleTitle = "请假申请"
    res = dict(leave_type=list(leave_type_choice))

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)
