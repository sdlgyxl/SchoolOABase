# -*- coding: utf-8 -*-
"""
@File    : views_nocheckin.py
@Time    : 2019-09-01 19:46
@Author  : 杨小林
"""
from django.utils.timezone import now
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import get_user_model
from .views_mixin import AttendanceListView, AttendanceApplyView, AttendanceDeleteView, AttendanceProcessView
from .models import NoCheckIn, check_in_period_choices
from system.mixin import LoginRequiredMixin
from .forms import NoCheckInApplyForm
from tools.funcs import get_prev_month
from base.models import Department

User = get_user_model()


class NoCheckInView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance/index.html'

    def get_context_data(self):
        self.kwargs['moduleName'] = '缺打卡申请'
        query_month = now()
        months = []
        for i in range(0, 12):
            months.append(query_month.strftime('%Y-%m'))
            query_month = get_prev_month(query_month)[0]
        self.kwargs['months'] = months
        self.kwargs['departments'] = Department.objects.all().values(*['id', 'name'])
        self.kwargs['users'] = User.objects.filter(is_active=1).values(*['id', 'name'])
        self.kwargs['moduleUrl'] = 'nocheckin'
        self.kwargs['not_agree_col'] = 8
        self.kwargs['columns'] = [{"title": "ID", "data": "id", "width": "6%"},
                                  {"title": "申请人", "data": "applicant__name", },
                                  {"title": "缺打卡时间", "data": "missing_time"},
                                  {"title": "打卡时段", "data": "check_in_period"},
                                  {"title": "缺打卡原因", "data": "reason", "width": '20%'},
                                  {"title": "缺打卡事由", "data": "witness", "width": '20%'},
                                  {"title": "当前步骤", "data": "step"},
                                  {"title": "处理人", "data": "auditor__name"},
                                  {"title": "申请结果", "data": "result"}]
        return super().get_context_data(**self.kwargs)


class NoCheckInListView(AttendanceListView):
    model = NoCheckIn
    fields = ['id', 'missing_time', 'check_in_period', 'reason', 'witness', 'applicant__name',
              'auditor__name', 'step', 'result', 'crdate']
    perm_all = 'attendance.view_all_nocheckin'
    perm_department = 'attendance.view_deprtment_nocheckin'
    key2values = ['step', 'result', 'check_in_period']
    selects = [['month', 'missing_time__startswith'], ['dept', 'applicant__department__id'], ['user', 'applicant__id']]

    def get(self, request):
        return super().get(request)


class NoCheckInApplyView(PermissionRequiredMixin, AttendanceApplyView):
    """
    申请
    """
    permission_required = ('attendance.add_nocheckin',)
    moduleName = "nocheckin"
    moduleTitle = "缺打卡申请"
    form = NoCheckInApplyForm
    moduleId = 1

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)


class NoCheckInDeleteView(AttendanceDeleteView):
    model = NoCheckIn
    moduleId = 1

    def post(self, request):
        return super().post(request)


class NoCheckInProcessView(AttendanceProcessView):
    """
    审批
    """
    model = NoCheckIn
    moduleId = 1
    moduleName = "nocheckin"
    moduleTitle = "缺打卡申请"
    res = dict(check_in_period=list(check_in_period_choices))

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)
