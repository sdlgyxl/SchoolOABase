import json
from django.views.generic import View
from django.shortcuts import render, HttpResponse
from .models import Instructor
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import get_user_model

User = get_user_model


class IndexView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('未登录')
        else:
            if request.user.has_perm('base.add_department'):
                return HttpResponse('已登录，具有增加部门权限')
            else:
                return HttpResponse('已登录，没有增加部门权限！！！！！！')


class DemoView(View):

    def get(self, request):
        return HttpResponse('这是DemoView，具有增加部门权限')


@permission_required('car.drive_car')
def demo(request):
    return HttpResponse('Demo, 具有增加部门权限')


'''
def index(request):
    res = dict(result=False)
    if not request.user.is_authenticated():
        return HttpResponse(json.dumps(res), content_type='application/json')
    # if request.user.has_perm('blog.create_discussion')：
    res['perm'] = request.user.permissions
    return HttpResponse(json.dumps(res), content_type='application/json')
'''
