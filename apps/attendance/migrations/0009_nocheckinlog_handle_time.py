# Generated by Django 2.1.5 on 2019-09-03 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0008_auto_20190903_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='nocheckinlog',
            name='handle_time',
            field=models.DateTimeField(null=True, verbose_name='处理时间'),
        ),
    ]