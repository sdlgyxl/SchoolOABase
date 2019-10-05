# -*- coding: utf-8 -*-
"""
@File    : forms.py
@Time    : 2019-08-27 15:31
@Author  : 杨小林
"""
import re
from django import forms
from . import models

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = ['name', 'description', 'parent']
