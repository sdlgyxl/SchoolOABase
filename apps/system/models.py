from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.models import Group, Permission


class Menu(models.Model):
    """
    菜单
    """
    name = models.CharField(max_length=30, unique=True, verbose_name='菜单名')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='父菜单')
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name='图标')
    url = models.CharField(max_length=128, null=True, blank=True, verbose_name='链接')
    number = models.CharField(max_length=20, null=True, blank=True, verbose_name="编号")
    # code = models.CharField(max_length=30, unique=True, default='', verbose_name='编码')
    groups = models.ManyToManyField(to=Group, verbose_name="角色")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        ordering = ['number']

    @classmethod
    def get_menu_by_request(cls, url):
        return dict(menu=Menu.objects.get(url=url))

    @classmethod
    def get_menu_by_request_url(cls, url):
        try:
            return dict(menu=Menu.objects.get(url=url))
        except:
            return None


class Instructor(AbstractUser):
    '''
    用户
    '''
    name = models.CharField(max_length=20, default='', verbose_name='姓名')
    gender = models.CharField(max_length=2, choices=(('男', '男'), ('女', '女')), default='男', verbose_name='性别')
    mobile = models.CharField(max_length=11, unique=True, default='', verbose_name='手机号')
    email = models.EmailField(max_length=30, verbose_name='邮箱')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期')
    headimage = models.ImageField(upload_to='images/instructor/headimage', default='images/default.jpg', max_length=100,
                                  null=True, blank=True, verbose_name='头像')
    department = models.ForeignKey('base.Department', null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name='部门')
    post = models.CharField(max_length=50, null=True, blank=True, verbose_name='职位')
    is_manager = models.BooleanField(default=False, verbose_name='是部门经理')
    superior = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='上级主管')
    private_password = models.CharField(max_length=128, null=True, verbose_name='私有密码')

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name
        ordering = ['id']

        permissions = (
            ("change_password", "基础数据.教师.修改密码"),
            ("enable_user", "基础数据.教师.启用用户"),
            ("disable_user", "基础数据.教师.禁用用户"),
        )

    def __str__(self):
        return self.name + ' ' + self.gender + ' '  # + self.department.name + self.mobile + ' ' + self.email
