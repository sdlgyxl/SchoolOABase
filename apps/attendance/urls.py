# -*- coding: utf-8 -*-
"""
@File    : urls.py
@Time    : 2019-08-30 16:09
@Author  : 杨小林
"""
from django.urls import path
from . import views, views_nocheckin, views_leave, views_overtime, views_outwork

app_name = 'attendance'

urlpatterns = [
    path('nocheckin/', views_nocheckin.NoCheckInView.as_view(), name='nocheckin'),
    path('nocheckin/list/', views_nocheckin.NoCheckInListView.as_view(), name='nocheckin-list'),
    path('nocheckin/apply/', views_nocheckin.NoCheckInApplyView.as_view(), name='nocheckin-apply'),
    path('nocheckin/process/', views_nocheckin.NoCheckInProcessView.as_view(), name='nocheckin-process'),
    path('nocheckin/delete/', views_nocheckin.NoCheckInDeleteView.as_view(), name='nocheckin-nocheckin'),

    path('leave/', views_leave.LeaveView.as_view(), name='leave'),
    path('leave/list/', views_leave.LeaveListView.as_view(), name='leave-list'),
    path('leave/apply/', views_leave.LeaveApplyView.as_view(), name='leave-apply'),
    path('leave/process/', views_leave.LeaveProcessView.as_view(), name='leave-process'),
    path('leave/delete/', views_leave.LeaveDeleteView.as_view(), name='leave-delete'),

    path('overtime/', views_overtime.OverTimeView.as_view(), name='overtime'),
    path('overtime/list/', views_overtime.OverTimeListView.as_view(), name='overtime-list'),
    path('overtime/apply/', views_overtime.OverTimeApplyView.as_view(), name='overtime-apply'),
    path('overtime/process/', views_overtime.OverTimeProcessView.as_view(), name='overtime-process'),
    path('overtime/delete/', views_overtime.OverTimeDeleteView.as_view(), name='overtime-delete'),

    path('outwork/', views_outwork.OutWorkView.as_view(), name='outwork'),
    path('outwork/list/', views_outwork.OutWorkListView.as_view(), name='outwork-list'),
    path('outwork/apply/', views_outwork.OutWorkApplyView.as_view(), name='outwork-apply'),
    path('outwork/process/', views_outwork.OutWorkProcessView.as_view(), name='outwork-process'),
    path('outwork/delete/', views_outwork.OutWorkDeleteView.as_view(), name='outwork-delete'),

]
