# -*- coding: utf-8 -*-
"""
@File    : urls.py
@Time    : 2019-08-27 13:08
@Author  : 杨小林
"""
from django.urls import path
from . import views_department
from django.contrib.auth.decorators import login_required, permission_required

app_name = 'base'
urlpatterns = [
    path('department/', views_department.DepartmentView.as_view(), name='department'),
    path('department/list/', views_department.DepartmentListView.as_view(), name='department-list'),
    path('department/edit/', views_department.DepartmentEditView.as_view(), name='department-edit'),
    path('department/delete/', views_department.DepartmentDeleteView.as_view(), name='department-delete'),
    path('department/add_instructor/', views_department.Department2InstructorView.as_view(), name='department-add_instructor'),

]
