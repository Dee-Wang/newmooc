# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-23 20:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20170517_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forget_password', '忘记密码'), ('change_email', '修改邮箱')], default='register', max_length=64, verbose_name='验证类型'),
        ),
    ]