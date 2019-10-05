from django.db import models


class Department(models.Model):
    '''
    部门,组织结构
    '''
    name = models.CharField(max_length=60, unique=True, verbose_name='部门名称')
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name='部门说明')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='上级部门')

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
