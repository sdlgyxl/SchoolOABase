# -*- coding: utf-8 -*-
"""
@File    : forms.py
@Time    : 2019-09-01 19:46
@Author  : 杨小林
"""
import re
from django import forms
from . import models
from datetime import datetime


class NoCheckInApplyForm(forms.ModelForm):
    class Meta:
        model = models.NoCheckIn
        fields = ['missing_time', 'check_in_period', 'reason', 'witness',
                  'auditor', 'step', 'result', 'applicant'
                  ]

        error_messages = {
            "missing_time": {"required": "缺打卡时间不能为空"},
            "check_in_period": {"required": "缺打卡时段不能为空"},
            "reason": {"required": "缺打卡原因不能为空"},
            "witness": {"required": "缺打卡事由不能为空"}
        }


class LeaveApplyForm(forms.ModelForm):
    class Meta:
        model = models.Leave
        fields = '__all__'

        error_messages = {
            'start_time': {'required': '开始时间不能为空'},
            'end_time': {'required': '结束时间不能为空'},
            'leave_type': {'required': '请假类型不能为空'},
            'reason': {'required': '请假原因不能为空'}
        }

    def clean(self):
        cleaned_data = super(LeaveApplyForm, self).clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        reason = cleaned_data.get("reason", "")
        leave_type = cleaned_data.get("leave_type")
        leave_hours = cleaned_data.get("leave_hours")
        crdate = datetime.now()

        if start_time > end_time:
            raise forms.ValidationError("结束时间必须晚于开始时间")


class OverTimeApplyForm(forms.ModelForm):
    class Meta:
        model = models.OverTime
        fields = '__all__'

        error_messages = {
            'start_time': {'required': '开始时间不能为空'},
            'end_time': {'required': '结束时间不能为空'},
            'overtime_type': {'required': '请假类型不能为空'},
            'reason': {'required': '请假原因不能为空'}
        }

    def clean(self):
        cleaned_data = super(OverTimeApplyForm, self).clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        reason = cleaned_data.get("reason", "")
        overtime_hours = cleaned_data.get("overtime_hours")
        crdate = datetime.now()

        if start_time > end_time:
            raise forms.ValidationError("结束时间必须晚于开始时间")


class OutWorkApplyForm(forms.ModelForm):
    class Meta:
        model = models.OutWork
        fields = '__all__'

        error_messages = {
            'start_time': {'required': '开始时间不能为空'},
            'end_time': {'required': '结束时间不能为空'},
            'address': {'required': '外勤地点不能为空'},
            'reason': {'required': '外勤原因不能为空'}
        }

    def clean(self):
        cleaned_data = super(OutWorkApplyForm, self).clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        reason = cleaned_data.get("reason", "")
        address = cleaned_data.get("address", "")
        outwork_hours = cleaned_data.get("outwork_hours")
        crdate = datetime.now()

        if start_time > end_time:
            raise forms.ValidationError("结束时间必须晚于开始时间")
