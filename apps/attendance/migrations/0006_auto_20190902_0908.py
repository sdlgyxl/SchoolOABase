# Generated by Django 2.1.5 on 2019-09-02 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_auto_20190901_1803'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nocheckin',
            old_name='appler',
            new_name='applicant',
        ),
    ]