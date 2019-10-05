# -*- coding: utf-8 -*-
"""
@File    : menus.py
@Time    : 2019-08-30 9:12
@Author  : 杨小林
"""
import re, json
from django.shortcuts import render, HttpResponse
from django.views.generic import View


class MenuCollection(View):
    def get_user(self, request):
        return request.user

    def get_menu_from_group(self, request, user=None):
        if user is None:
            user = self.get_user(request)
        try:
            menus = user.groups.values(
                'menu__id',
                'menu__name',
                'menu__url',
                'menu__icon',
                'menu__parent',
                'menu__number'
            ).distinct().order_by('menu__number')
            return [menu for menu in menus if menu['menu__id'] is not None]
        except AttributeError:
            return None

    def get_basic_menus(self, request):
        basic_menu_list = []
        group_menus = self.get_menu_from_group(request)
        if group_menus is not None:
            for item in group_menus:
                menu = {
                    'id': item['menu__id'],
                    'name': item['menu__name'],
                    'url': item['menu__url'],
                    'icon': item['menu__icon'],
                    'parent': item['menu__parent'],
                    'status': False,
                    'sub_menu': [],
                }
                basic_menu_list.append(menu)
            return basic_menu_list

    def get_tree_menus(self, request):
        menus_dict = {}
        request_url = request.path_info
        menus_list = self.get_basic_menus(request)
        if menus_list is not None:
            for menu in menus_list:
                url = menu['url']
                if url and re.match(url, request_url):
                    menu['status'] = True
                menus_dict[menu['id']] = menu

            tree_menus = []
            for i in menus_dict:
                if menus_dict[i]['parent']:
                    pid = menus_dict[i]['parent']
                    parent_menu = menus_dict[pid]
                    parent_menu['sub_menu'].append(menus_dict[i])
                else:
                    tree_menus.append(menus_dict[i])
            return tree_menus

    def get_my_menu(self, request):
        tree_menus = self.get_tree_menus(request)
        menu_str = ''
        if tree_menus:
            for a_menu in tree_menus:
                menu_str += '<li><a href="' + (a_menu['url'] if a_menu['url'] else '#') + '">'
                if a_menu['icon']:
                    menu_str += '<i class ="' + a_menu['icon'] + '"></i>'
                menu_str += '<span class="nav-label">' + a_menu['name'] + '</span>'
                if a_menu['sub_menu']:
                    menu_str += '<span class="fa arrow"></span>'
                menu_str += '</a>'
                if a_menu['sub_menu']:
                    menu_str += '<ul class="nav nav-second-level collapse">'
                    for b_menu in a_menu['sub_menu']:
                        menu_str += '<li><a href="' + (b_menu['url'] if b_menu['url'] else '#') + '">'
                        if b_menu['icon']:
                            menu_str += '<i class="' + b_menu['icon'] + '"></i>'
                        menu_str += b_menu['name']
                        if b_menu['sub_menu']:
                            menu_str += '<span class="fa arrow"></span>'
                        menu_str += '</a>'
                        if b_menu['sub_menu']:
                            menu_str += '<ul class="nav nav-third-level">'
                            for c_menu in b_menu['sub_menu']:
                                menu_str += '<li><a href="' + c_menu['url'] + '">' + c_menu['name'] + '</a></li>'
                            menu_str += '</ul>'
                        menu_str += '</li>'
                    menu_str += '</ul>'
                menu_str += '</li>'
            request.session['tree_menus'] =json.dumps(tree_menus)
            request.session['my_menu_string'] = menu_str
