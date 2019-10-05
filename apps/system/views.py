import json, re
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views.generic.base import View, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.db.models import Q
from .mixin import LoginRequiredMixin
from .forms import LoginForm
from tools.my_menus import MenuCollection

User = get_user_model()


class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'system/index.html')


class LoginView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'system/login.html')
        else:
            return HttpResponseRedirect(reverse('system-index'))

    def post(self, request):
        redirect_to = request.GET.get('next', '/')
        login_form = LoginForm(request.POST)
        res = dict(login_form=login_form)
        print(request.META.get('REMOTE_ADDR'))
        if login_form.is_valid():
            user_name = request.POST['username']
            pass_word = request.POST['password']
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    my_menu = MenuCollection()
                    my_menu.get_my_menu(request)
                    return HttpResponseRedirect(redirect_to)
                else:
                    res['msg'] = '用户未激活！'
            else:
                res['msg'] = '用户名或密码错误！'
        else:
            res['msg'] = '用户和密码不能为空！'
        return render(request, 'system/login.html', res)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))




def mytest(request):
    return render(request, 'mytest.html')
