# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-10 15:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_auto_20170508_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_tag',
            field=models.CharField(default='', max_length=64, verbose_name='课程标签'),
        ),
    ]
