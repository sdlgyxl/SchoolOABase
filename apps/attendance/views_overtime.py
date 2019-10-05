# -*- coding: utf-8 -*-
"""
@File    : views_overtime.py
@Time    : 2019-09-06 14:48
@Author  : 杨小林
"""
from django.views.generic import TemplateView, View
from django.utils.timezone import now
from tools.funcs import get_prev_month
from system.mixin import LoginRequiredMixin
from .views_mixin import AttendanceListView, AttendanceApplyView, AttendanceDeleteView, AttendanceProcessView
from .models import OverTime
from base.models import Department
from django.contrib.auth import get_user_model
from .forms import OverTimeApplyForm
from django.contrib.auth.mixins import PermissionRequiredMixin

User = get_user_model()


class OverTimeView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance/index.html'

    def get_context_data(self):
        self.kwargs['moduleName'] = '加班申请'
        query_month = now()
        months = []
        for i in range(0, 12):
            months.append(query_month.strftime('%Y-%m'))
            query_month = get_prev_month(query_month)[0]
        self.kwargs['months'] = months
        self.kwargs['departments'] = Department.objects.all().values(*['id', 'name'])
        self.kwargs['users'] = User.objects.filter(is_active=1).values(*['id', 'name'])
        self.kwargs['moduleUrl'] = 'overtime'
        self.kwargs['not_agree_col'] = 8
        self.kwargs['columns'] = [{"title": "ID", "data": "id"},
                                  {"title": "申请人", "data": "applicant__name"},
                                  {"title": "开始时间", "data": "start_time"},
                                  {"title": "结束时间", "data": "end_time"},
                                  {"title": "加班时长", "data": "overtime_hours"},
                                  {"title": "加班原因", "data": "reason"},
                                  {"title": "审批步骤", "data": "step"},
                                  {"title": "审批人", "data": "auditor__name"},
                                  {"title": "审批结果", "data": "result"}]
        return super().get_context_data(**self.kwargs)


class OverTimeListView(AttendanceListView):
    model = OverTime
    fields = ['id', 'applicant__name', 'start_time', 'end_time',
              "overtime_hours", "reason", "step", "auditor__name", "result"]
    perm_all = 'attendance.view_all_overtime'
    perm_department = 'attendance.view_deprtment_overtime'
    key2values = ['step', 'result']
    selects = [['month', 'start_time__startswith'], ['dept', 'applicant__department__id'], ['user', 'applicant__id']]

    def get(self, request):
        return super().get(request)


class OverTimeApplyView(PermissionRequiredMixin, AttendanceApplyView):
    permission_required = ('attendance.add_overtime',)
    moduleName = "overtime"
    moduleTitle = "加班申请"
    form = OverTimeApplyForm
    moduleId = 3

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)


class OverTimeDeleteView(AttendanceDeleteView):
    model = OverTime
    moduleId = 3

    def post(self, request):
        return super().post(request)


class OverTimeProcessView(AttendanceProcessView):
    """
    审批
    """
    model = OverTime
    moduleId = 3
    moduleName = "overtime"
    moduleTitle = "加班申请"
    def get(self, request):

        return super().get(request)

    def post(self, request):
        return super().post(request)


'''
class OverTimeProcessView(LoginRequiredMixin, View):
    """
    审批
    """

    def get(self, request):
        user = request.user
        position = '员工'
        if user.groups.filter(name='部门主管'):
            position = '部门主管'
        elif user.groups.filter(name='校区主任'):
            position = '校区主任'
        id = int(request.GET['id'])
        overtime = get_object_or_404(OverTime, pk=id)
        fields = ['id', 'auditor__name', 'is_agree', 'opinion', 'view_time', 'crdate', 'process_time']
        logs = AttendanceLog.objects.filter(module_id=moduleId).filter(relate_id=overtime.id).order_by(
            'relate_id').values(
            *fields)
        res = dict(data=overtime, position=position, logs=logs, moduleName="overtime",
                   applyUrl="/attendance/overtime/process/", moduleTitle="加班申请")
        write_view_date(moduleId, id, user.id)
        return render(request, 'attendance/attendance-process.html', res)

    def post(self, request):
        overtime = get_object_or_404(OverTime, pk=int(request.POST['id']))
        user = request.user
        if int(user.id) == overtime.auditor.id:
            is_agree = int(request.POST.get('is_agree'))
            if is_agree == 2:
                overtime.result = 2
                overtime.auditor = None
            else:
                overtime.step += 1
                overtime.auditor = user.superior
                if overtime.step == 4:
                    if is_agree == 1:
                        overtime.result = 1
                    else:
                        overtime.result = 2
                    overtime.auditor = None
                else:
                    overtime.result = 0
            overtime.save()
            if user.groups.filter(name__in=['部门主管', '校区主任']):  # 提交校区主任
                # 加班申请记录,保存当前操作 def write_process(id, userId, module_id, is_agree, opinion):
                write_process(moduleId, overtime.id, user.id, is_agree, request.POST.get('opinion'))
                # 添加一条审批记录
                if overtime.step < 4 and is_agree < 2:
                    add_a_attendancelog(moduleId, overtime.id, overtime.auditor, overtime.step, 0, None, None)
                # 短信通知cur_handler,applicant
            res = {'result': 'success'}
        else:
            res = {'result': 'fail', 'error_messages': '没有操作的权限！'}
        return HttpResponse(json.dumps(res), content_type='application/json')
class OverTimeDeleteView2(LoginRequiredMixin, View):
    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id = int(request.POST['id'])
            overtime = OverTime.objects.filter(id=id)[0]
            if overtime.applicant.id == request.user.id and overtime.result == 0 and overtime.step < 4:
                overtime.delete()
                AttendanceLog.objects.filter(module_id=moduleId, relate_id=id).delete()
                res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


class OverTimeApplyView2(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    添加
    """
    permission_required = ('attendance.add_overtime',)

    def get(self, request):
        user = request.user
        step = 2
        if user.groups.filter(name='部门主管'):
            step = 3
        res = dict(step=step, moduleName="overtime", applyUrl="/attendance/overtime/apply/", moduleTitle="加班申请")
        return render(request, 'attendance/attendance-apply.html', res)

    def post(self, request):
        overtime_apply_form = OverTimeApplyForm(request.POST)
        user = request.user
        if overtime_apply_form.is_valid():
            overtime_apply_form.save()
            overtime = overtime_apply_form.instance
            # 加班申请记录，添加一条申请纪录
            add_a_attendancelog(moduleId, overtime.id, user, 1, 1, now(), now())
            # 添加一条审批记录
            add_a_attendancelog(moduleId, overtime.id, overtime.auditor, overtime.step, 0, None, None)
            # 短信通知cur_processer
            res = {'result': True}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(overtime_apply_form.errors)
            error_messages = re.findall(pattern, errors)
            res = {
                'result': False,
                'error_messages': error_messages[0]
            }
        return HttpResponse(json.dumps(res), content_type='application/json')

'''
