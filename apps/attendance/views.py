from django.shortcuts import render
from django.views.generic import View


class H1View(View):

    def get(self, request):
        return render(request, 'attendance/h1.html')


class H2View(View):

    def get(self, request):
        return render(request, 'attendance/h2.html')

class OutWorkView(View):

    def get(self, request):
        return render(request, 'attendance/outwork.html')
