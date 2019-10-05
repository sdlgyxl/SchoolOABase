import datetime, time
from django.utils.timezone import now
from django.db import models
from django.contrib.auth import get_user_model

Instructor = get_user_model()

check_in_period_choices = ((1, '上午上班'), (2, '上午下班'), (3, '下午上班'), (4, '下午下班'))
step_choices = ((1, '提出申请'), (2, '部门主管处理'), (3, '校区主任处理'), (4, '审批完毕'))
result_choices = ((0, '处理中...'), (1, '同意'), (2, '不同意'))
is_agree_choices = ((0, '未审核'), (1, '同意'), (2, '不同意'))
leave_type_choice = ((1, '病假'), (2, '事假'), (3, '婚假'), (4, '产假'), (5, '父亲假'), (6, '工伤假'), (7, '丧假'), (8, '调休'))
module_choices = ((1, '缺打卡'), (2, '请假'), (3, '加班'), (4, '外勤'), (5, '出差'), (6, '调休'))


class NoCheckIn(models.Model):
    """
    忘打卡申请
    """
    applicant = models.ForeignKey(Instructor, on_delete=models.CASCADE, verbose_name='申请人',
                                  related_name='no_check_in_applyer')
    missing_time = models.DateTimeField(verbose_name='缺打卡时间')
    check_in_period = models.IntegerField(choices=check_in_period_choices, verbose_name='打卡时段')
    reason = models.CharField(max_length=256, verbose_name='缺打卡原因')
    witness = models.CharField(max_length=256, verbose_name="缺打卡事由")
    auditor = models.ForeignKey(Instructor, null=True, on_delete=models.CASCADE,
                                related_name='no_check_in_auditor', verbose_name='应审核人')
    step = models.IntegerField(choices=step_choices, verbose_name='处理步骤')
    result = models.IntegerField(choices=result_choices, verbose_name='审核结果')
    crdate = models.DateTimeField(default=now, verbose_name='创建时间')

    def __str__(self):
        return self.applicant.name

    class Meta:
        verbose_name = '缺打卡申请'
        verbose_name_plural = verbose_name

        permissions = (
            ("process_nocheckin", "行政人事.考勤管理.缺打卡.处理申请"),
            ("view_all_nocheckin", "行政人事.考勤管理.缺打卡.查看所有申请"),
            ("view_deprtment_nocheckin", "行政人事.考勤管理.缺打卡.查看本部门申请"),
        )


class AttendanceLog(models.Model):
    """
    考勤相关模块操作记录
    """
    module_id = models.IntegerField(choices=module_choices, verbose_name='模块ID')
    relate_id = models.IntegerField(null=False, verbose_name='关联申请ID')
    auditor = models.ForeignKey(Instructor, null=True, on_delete=models.SET_NULL, verbose_name='审批人')
    step = models.CharField(max_length=2, choices=step_choices, verbose_name='步骤')
    view_time = models.DateTimeField(null=True, verbose_name='查看时间')
    process_time = models.DateTimeField(null=True, verbose_name='处理时间')
    is_agree = models.IntegerField(null=True, choices=is_agree_choices, verbose_name='是否同意')
    opinion = models.CharField(max_length=256, null=True, verbose_name='审核意见')
    crdate = models.DateTimeField(default=now, verbose_name='创建时间')


class Leave(models.Model):
    """
    请假申请
    """
    applicant = models.ForeignKey(Instructor, on_delete=models.CASCADE, verbose_name='申请人',
                                  related_name='leave_applicant')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    leave_hours = models.DecimalField(max_digits=5, decimal_places=1, null=True, verbose_name='请假时长')
    leave_type = models.IntegerField(choices=leave_type_choice, verbose_name='请假类型')
    reason = models.CharField(max_length=256, verbose_name="请假原因")
    auditor = models.ForeignKey(Instructor, null=True, on_delete=models.CASCADE, verbose_name='审核人',
                                related_name='leave_auditor')
    step = models.IntegerField(choices=step_choices, verbose_name='处理步骤')
    result = models.IntegerField(choices=result_choices, verbose_name='审核结果')
    crdate = models.DateTimeField(default=now, verbose_name='创建时间')

    def __str__(self):
        return self.applicant.name

    class Meta:
        verbose_name = '请假申请'
        verbose_name_plural = verbose_name

        permissions = (
            ("process_leave", "行政人事.考勤管理.请假.处理申请"),
            ("view_all_leave", "行政人事.考勤管理.请假.查看所有申请"),
            ("view_deprtment_leave", "行政人事.考勤管理.请假.查看本部门申请"),
        )


class OverTime(models.Model):
    """
    请假申请
    """
    applicant = models.ForeignKey(Instructor, on_delete=models.CASCADE, verbose_name='申请人',
                                  related_name='overtime_applicant')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=1, null=True, verbose_name='加班时长')
    reason = models.CharField(max_length=256, verbose_name="加班原因")
    auditor = models.ForeignKey(Instructor, null=True, on_delete=models.CASCADE, verbose_name='审核人',
                                related_name='overtime_auditor')
    step = models.IntegerField(choices=step_choices, verbose_name='处理步骤')
    result = models.IntegerField(choices=result_choices, verbose_name='审核结果')
    crdate = models.DateTimeField(default=now, verbose_name='创建时间')

    def __str__(self):
        return self.applicant.name

    class Meta:
        verbose_name = '加班申请'
        verbose_name_plural = verbose_name

        permissions = (
            ("process_overtime", "行政人事.考勤管理.加班.处理申请"),
            ("view_all_overtime", "行政人事.考勤管理.加班.查看所有申请"),
            ("view_deprtment_overtime", "行政人事.考勤管理.加班.查看本部门申请"),
        )


class OutWork(models.Model):
    """
    请假申请
    """
    applicant = models.ForeignKey(Instructor, on_delete=models.CASCADE, verbose_name='申请人',
                                  related_name='outwork_applicant')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    outwork_hours = models.DecimalField(max_digits=5, decimal_places=1, null=True, verbose_name='外勤时长')
    address = models.CharField(max_length=256, verbose_name='外勤地点')
    reason = models.CharField(max_length=256, verbose_name="外勤原因")
    auditor = models.ForeignKey(Instructor, null=True, on_delete=models.CASCADE, verbose_name='审核人',
                                related_name='outwork_auditor')
    step = models.IntegerField(choices=step_choices, verbose_name='处理步骤')
    result = models.IntegerField(choices=result_choices, verbose_name='审核结果')
    crdate = models.DateTimeField(default=now, verbose_name='创建时间')

    def __str__(self):
        return self.applicant.name

    class Meta:
        verbose_name = '外勤申请'
        verbose_name_plural = verbose_name

        permissions = (
            ("process_outwork", "行政人事.考勤管理.外勤.处理申请"),
            ("view_all_outwork", "行政人事.考勤管理.外勤.查看所有申请"),
            ("view_deprtment_outwork", "行政人事.考勤管理.外勤.查看本部门申请"),
        )


class BusinessTrip(models.Model):
    """
    出差申请
    """
    applicant = models.ForeignKey(Instructor, on_delete=models.CASCADE, verbose_name='申请人',
                                  related_name='businesstrip_applicant')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    destination = models.CharField(max_length=256, verbose_name='目的地')
    reason = models.CharField(max_length=256, verbose_name="出差原因")
    expected_result = models.CharField(max_length=512, verbose_name="预计归来的结果")
    required_support = models.CharField(max_length=512, verbose_name="所需支持")
    auditor = models.ForeignKey(Instructor, null=True, on_delete=models.CASCADE, verbose_name='审核人',
                                related_name='businesstrip_auditor')
    step = models.IntegerField(choices=step_choices, verbose_name='处理步骤')
    result = models.IntegerField(choices=result_choices, verbose_name='审核结果')
    crdate = models.DateTimeField(default=now, verbose_name='创建时间')

    def __str__(self):
        return self.applicant.name

    class Meta:
        verbose_name = '出差申请'
        verbose_name_plural = verbose_name

        permissions = (
            ("process_businesstrip", "行政人事.考勤管理.出差.处理申请"),
            ("view_all_businesstrip", "行政人事.考勤管理.出差.查看所有申请"),
            ("view_deprtment_businesstrip", "行政人事.考勤管理.出差.查看本部门申请"),
        )


class BreakOff(models.Model):
    """
    调休申请
    """
    applicant = models.ForeignKey(Instructor, on_delete=models.CASCADE, verbose_name='申请人',
                                  related_name='breakoff_applicant')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    breakoff_hours = models.DecimalField(max_digits=5, decimal_places=1, null=True, verbose_name='调休时长')
    reason = models.CharField(max_length=256, verbose_name="调休原因")
    auditor = models.ForeignKey(Instructor, null=True, on_delete=models.CASCADE, verbose_name='审核人',
                                related_name='breakoff_auditor')
    step = models.IntegerField(choices=step_choices, verbose_name='处理步骤')
    result = models.IntegerField(choices=result_choices, verbose_name='审核结果')
    crdate = models.DateTimeField(default=now, verbose_name='创建时间')

    def __str__(self):
        return self.applicant.name

    class Meta:
        verbose_name = '调休申请'
        verbose_name_plural = verbose_name

        permissions = (
            ("process_breakoff", "行政人事.考勤管理.调休.处理申请"),
            ("view_all_breakoff", "行政人事.考勤管理.调休.查看所有申请"),
            ("view_deprtment_breakoff", "行政人事.考勤管理.调休.查看本部门申请"),
        )


class Vacation(models.Model):
    '''假期信息'''

    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, verbose_name='员工',
                                   related_name='vacation_instructor')
    remaining_time = models.DecimalField(max_digits=5, decimal_places=1, null=True, verbose_name='剩余调休时长')
    adjust_time = models.DecimalField(max_digits=5, decimal_places=1, null=True, verbose_name='本次调整时长')
    auditor = models.ForeignKey(Instructor, on_delete=models.CASCADE, verbose_name='审核人',
                                related_name='vacation_auditor')
    adjust_reason = models.CharField(max_length=256, verbose_name='调整原因')
    crdate = models.DateTimeField(default=now, verbose_name='创建时间')

    def __str__(self):
        return self.instructor.name

    class Meta:
        verbose_name = '调休信息'
        verbose_name_plural = verbose_name

        permissions = (
            ("view_all_Vacation", "行政人事.考勤管理.调休信息.查看所有"),
            ("view_deprtment_Vacation", "行政人事.考勤管理.调休信息.查看本部门"),
        )


class VacationLog(models.Model):
    '''假期信息'''

    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, verbose_name='员工',
                                   related_name='vacationlog_instructor')
    remaining_time = models.DecimalField(max_digits=5, decimal_places=1, null=True, verbose_name='剩余调休时长')
    adjust_time = models.DecimalField(max_digits=5, decimal_places=1, null=True, verbose_name='本次调整时长')
    auditor = models.ForeignKey(Instructor, on_delete=models.CASCADE, verbose_name='审核人',
                                related_name='vacationlog_auditor')
    adjust_reason = models.CharField(max_length=256, verbose_name='调整原因')
    crdate = models.DateTimeField(default=now, verbose_name='创建时间')

    def __str__(self):
        return self.instructor.name
