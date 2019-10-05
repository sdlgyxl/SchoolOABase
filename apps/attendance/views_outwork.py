# -*- coding: utf-8 -*-
"""
@File    : views_outwork.py
@Time    : 2019-09-06 14:48
@Author  : 杨小林
"""
from django.views.generic import TemplateView
from django.utils.timezone import now
from tools.funcs import get_prev_month
from system.mixin import LoginRequiredMixin
from .views_mixin import AttendanceListView, AttendanceApplyView, AttendanceDeleteView, AttendanceProcessView
from .models import OutWork
from base.models import Department
from django.contrib.auth import get_user_model
from .forms import OutWorkApplyForm
from django.contrib.auth.mixins import PermissionRequiredMixin

User = get_user_model()


class OutWorkView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance/index.html'

    def get_context_data(self):
        self.kwargs['moduleName'] = '外勤申请'
        query_month = now()
        months = []
        for i in range(0, 12):
            months.append(query_month.strftime('%Y-%m'))
            query_month = get_prev_month(query_month)[0]
        self.kwargs['months'] = months
        self.kwargs['departments'] = Department.objects.all().values(*['id', 'name'])
        self.kwargs['users'] = User.objects.filter(is_active=1).values(*['id', 'name'])
        self.kwargs['moduleUrl'] = 'outwork'
        self.kwargs['not_agree_col'] = 9
        self.kwargs['columns'] = [{"title": "ID", "data": "id"},
                                  {"title": "申请人", "data": "applicant__name"},
                                  {"title": "开始时间", "data": "start_time"},
                                  {"title": "结束时间", "data": "end_time"},
                                  {"title": "外勤时长", "data": "outwork_hours"},
                                  {"title": "外勤地点", "data": "address"},
                                  {"title": "外勤原因", "data": "reason"},
                                  {"title": "审批步骤", "data": "step"},
                                  {"title": "审批人", "data": "auditor__name"},
                                  {"title": "审批结果", "data": "result"}]
        return super().get_context_data(**self.kwargs)


class OutWorkListView(AttendanceListView):
    model = OutWork
    fields = ['id', 'applicant__name', 'start_time', 'end_time', "address",
              "outwork_hours", "reason", "step", "auditor__name", "result"]
    perm_all = 'attendance.view_all_outwork'
    perm_department = 'attendance.view_deprtment_outwork'
    key2values = ['step', 'result']
    selects = [['month', 'start_time__startswith'], ['dept', 'applicant__department__id'], ['user', 'applicant__id']]

    def get(self, request):
        return super().get(request)


class OutWorkApplyView(PermissionRequiredMixin, AttendanceApplyView):
    """
    添加
    """
    permission_required = ('attendance.add_outwork',)
    moduleName = "outwork"
    moduleTitle = "外勤申请"
    form = OutWorkApplyForm
    moduleId = 4

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)


class OutWorkDeleteView(AttendanceDeleteView):
    model = OutWork
    moduleId = 4

    def post(self, request):
        return super().post(request)


class OutWorkProcessView(AttendanceProcessView):
    """
    审批
    """

    model = OutWork
    moduleId = 4
    moduleName = "outwork"
    moduleTitle = "外勤申请"

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)
