# -*- coding: utf-8 -*-
"""
@File    : views_mixin.py
@Time    : 2019-09-06 9:37
@Author  : 杨小林
"""

import json, re
from django.utils.timezone import now
from django.views.generic import View
from django.shortcuts import HttpResponse, render, get_object_or_404
from tools.classes import DateEncoder
from system.mixin import LoginRequiredMixin
from .models import step_choices, result_choices, leave_type_choice, check_in_period_choices, AttendanceLog

dict_step = dict(step_choices)
dict_result = dict(result_choices)
dict_leave_type = dict(leave_type_choice)
dict_check_in_period = dict(check_in_period_choices)


class AttendanceListView(LoginRequiredMixin, View):
    """
    JsonResponse some json of objects, set by `self.model` or `self.queryset`.
    """
    fields = []
    filters = {}
    model = None
    perm_all = ''
    perm_department = ''
    key2values = []
    selects = []

    def get(self, request):
        # 获取筛选条件
        for item in self.selects:
            if item[0] in request.GET and request.GET[item[0]]:
                self.filters[item[1]] = request.GET[item[0]]
        filters = self.filters
        fields = self.fields
        qs = self.model.objects.filter(**filters)
        # 根据权限不同，进行筛选
        user = request.user
        if user.has_perm(self.perm_all):  # 查看全部
            pass
        elif user.has_perm(self.perm_department):  # 查看本部门
            qs = qs.filter(applicant__department__id=user.department.id)
        else:  # 查看自己的申请
            qs = qs.filter(applicant__id=user.id)
        # queryset 转成列表
        data = list(qs.order_by('-id').values(*fields))
        # 字典项，键改为值
        for item in data:
            for k in self.key2values:
                item[k] = eval("dict_" + k + "[item['" + k + "']]")

        # 提交结果
        context = dict(data=data)
        return HttpResponse(json.dumps(context, cls=DateEncoder), content_type='application/json')


def add_a_attendancelog(module_id, relate_id, auditor, step, is_agree, view_time, process_time):
    a_log = AttendanceLog()
    a_log.module_id = module_id
    a_log.relate_id = relate_id
    a_log.auditor = auditor
    a_log.step = step
    a_log.is_agree = is_agree
    a_log.process_time = process_time
    a_log.view_time = view_time
    a_log.save()


def write_view_date(module_id, id, userId):
    attendancelogs = AttendanceLog.objects.filter(module_id=module_id).filter(relate_id=id)
    if not attendancelogs:
        return
    attendancelog = attendancelogs.order_by('-id')[0]
    if not attendancelog.view_time:
        if attendancelog.auditor_id == userId:
            attendancelog.view_time = now()
            attendancelog.save()


def write_process(module_id, id, userId, is_agree, opinion):
    attendancelogs = AttendanceLog.objects.filter(module_id=module_id).filter(relate_id=id)
    if not attendancelogs:
        return
    a_log = attendancelogs.order_by('-id')[0]
    if not a_log.process_time:
        if a_log.auditor_id == userId:
            a_log.process_time = now()
            a_log.is_agree = is_agree
            a_log.opinion = opinion
            a_log.save()


class AttendanceApplyView(LoginRequiredMixin, View):
    """
    添加
    """
    moduleName = ""
    moduleTitle = ""
    form = None
    moduleId = 0
    res = {}

    def get(self, request):
        user = request.user
        step = 2
        if user.groups.filter(name='部门主管'):
            step = 3
        self.res['step'] = step
        self.res['moduleName'] = self.moduleName
        self.res['applyUrl'] = "/attendance/" + self.moduleName + "/apply/"
        self.res['moduleTitle'] = self.moduleTitle
        return render(request, 'attendance/attendance-apply.html', self.res)

    def post(self, request):
        apply_form = self.form(request.POST)
        user = request.user
        if apply_form.is_valid():
            apply_form.save()
            apply_model = apply_form.instance
            # 加班申请记录，添加一条申请纪录
            add_a_attendancelog(self.moduleId, apply_model.id, user, 1, 1, now(), now())
            # 添加一条审批记录
            add_a_attendancelog(self.moduleId, apply_model.id, apply_model.auditor, apply_model.step, 0, None, None)
            # 短信通知cur_processer
            res = {'result': True}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(apply_form.errors)
            error_messages = re.findall(pattern, errors)
            res = {
                'result': False,
                'error_messages': error_messages[0]
            }
        return HttpResponse(json.dumps(res), content_type='application/json')


class AttendanceDeleteView(LoginRequiredMixin, View):
    model = None
    moduleId = 0

    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id = int(request.POST['id'])
            delete_model = self.model.objects.filter(id=id)[0]
            if delete_model.applicant.id == request.user.id and delete_model.result == 0 and delete_model.step < 4:
                delete_model.delete()
                AttendanceLog.objects.filter(module_id=self.moduleId, relate_id=id).delete()
                res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


class AttendanceProcessView(LoginRequiredMixin, View):
    """
    审批
    """
    model = None
    moduleId = 0
    moduleName = ""
    moduleTitle = ""
    res = {}

    def get(self, request):
        user = request.user
        position = '员工'
        if user.groups.filter(name='部门主管'):
            position = '部门主管'
        elif user.groups.filter(name='校区主任'):
            position = '校区主任'
        id = int(request.GET['id'])

        process_model = get_object_or_404(self.model, pk=id)
        fields = ['id', 'auditor__name', 'is_agree', 'opinion', 'view_time', 'crdate', 'process_time']
        logs = AttendanceLog.objects.filter(module_id=self.moduleId, relate_id=process_model.id) \
            .order_by('relate_id').values(*fields)
        self.res['data'] = process_model
        self.res['position'] = position
        self.res['logs'] = logs
        self.res['moduleName'] = self.moduleName
        self.res['applyUrl'] = "/attendance/" + self.moduleName + "/process/"
        self.res['moduleTitle'] = self.moduleTitle
        write_view_date(self.moduleId, id, user.id)
        return render(request, 'attendance/attendance-process.html', self.res)

    def post(self, request):
        process_model = get_object_or_404(self.model, pk=int(request.POST['id']))
        user = request.user
        if int(user.id) == process_model.auditor.id:
            is_agree = int(request.POST.get('is_agree'))
            if is_agree == 2:
                process_model.result = 2
                process_model.auditor = None
            else:
                process_model.step += 1
                process_model.auditor = user.superior
                if process_model.step == 4:
                    if is_agree == 1:
                        process_model.result = 1
                    else:
                        process_model.result = 2
                    process_model.auditor = None
                else:
                    process_model.result = 0
            process_model.save()
            if user.groups.filter(name__in=['部门主管', '校区主任']):  # 提交校区主任
                # 加班申请记录,保存当前操作 def write_process(id, userId, module_id, is_agree, opinion):
                write_process(self.moduleId, process_model.id, user.id, is_agree, request.POST.get('opinion'))
                # 添加一条审批记录
                if process_model.step < 4 and is_agree < 2:
                    add_a_attendancelog(self.moduleId, process_model.id, process_model.auditor, process_model.step, 0,
                                        None, None)
                # 短信通知cur_handler,applicant
            res = {'result': 'success'}
        else:
            res = {'result': 'fail', 'error_messages': '没有操作的权限！'}
        return HttpResponse(json.dumps(res), content_type='application/json')
