# -*- coding: utf-8 -*-
"""
@File    : views_menu.py
@Time    : 2019-08-28 10:38
@Author  : 杨小林
"""
import json
from django.views.generic import ListView, View
from django.shortcuts import HttpResponse, render, get_object_or_404
from .mixin import LoginRequiredMixin
from .models import Menu
from . import forms

class MenuView(LoginRequiredMixin, ListView):
    model = Menu
    template_name = "system/menus/menu.html"


class MenuListView(LoginRequiredMixin, View):

    def get(self, request):
        fields = ['id', 'name', 'icon', 'url', 'number', 'parent__name']
        filters = dict()
        if 'select' in request.GET and request.GET['select']:
            filters['name'] = request.GET['select']
        res = dict(data=list(Menu.objects.filter(**filters).values(*fields)))
        return HttpResponse(json.dumps(res), content_type='application/json')


class MenuEditView(LoginRequiredMixin, View):

    def get(self, request):
        res = dict(menu_all=Menu.objects.all())
        if 'id' in request.GET and request.GET['id']:
            menu = get_object_or_404(Menu, pk=request.GET['id'])
            res['menu'] = menu
        return render(request, 'system/menus/menu-edit.html', res)

    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            menu = get_object_or_404(Menu, pk=request.POST['id'])
        else:
            menu = Menu()
        menu_form = forms.MenuForm(request.POST, instance=menu)
        if menu_form.is_valid():
            menu_form.save()
            res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


class MenuDeleteView(LoginRequiredMixin, View):
    """
    删除数据：支持删除单条记录和批量删除
    """

    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST['id'].split(','))
            Menu.objects.filter(id__in=id_list).delete()
            res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')
