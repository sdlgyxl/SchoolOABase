# Generated by Django 2.1.5 on 2019-09-06 14:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance', '0013_auto_20190906_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_id', models.IntegerField(choices=[(1, '缺打卡'), (2, '请假'), (3, '加班')], verbose_name='模块ID')),
                ('relate_id', models.IntegerField(verbose_name='关联申请ID')),
                ('step', models.CharField(choices=[(1, '提出申请'), (2, '部门主管处理'), (3, '校区主任处理'), (0, '审批完毕')], max_length=2, verbose_name='步骤')),
                ('view_time', models.DateTimeField(null=True, verbose_name='查看时间')),
                ('handle_time', models.DateTimeField(null=True, verbose_name='处理时间')),
                ('is_agree', models.IntegerField(choices=[(0, '未审核'), (1, '同意'), (2, '不同意')], null=True, verbose_name='是否同意')),
                ('opinion', models.CharField(max_length=256, null=True, verbose_name='审核意见')),
                ('crdate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('auditor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='审批人')),
            ],
        ),
        migrations.AlterField(
            model_name='nocheckinlog',
            name='is_agree',
            field=models.IntegerField(choices=[(0, '未审核'), (1, '同意'), (2, '不同意')], null=True, verbose_name='是否同意'),
        ),
    ]