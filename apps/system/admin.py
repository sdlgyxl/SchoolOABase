from django.contrib import admin
from django.contrib.auth.models import Permission
from . import models


class InstructorModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'gender', 'mobile', 'email']  # 展示的字段
    # list_editable = ['name', 'username', 'gender', 'mobile', 'email']


admin.site.register(models.Menu)
admin.site.register(models.Instructor, InstructorModelAdmin)
admin.site.register(Permission)
admin.site.site_title = "后台管理系统"
admin.site.site_header = "后台管理"
admin.site.index_title = "欢迎登陆"
