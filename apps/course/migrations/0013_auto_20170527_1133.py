# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-27 11:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0012_course_is_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=64, verbose_name='课程名'),
        ),
    ]
