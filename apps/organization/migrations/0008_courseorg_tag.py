# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-27 17:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_teacher_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='tag',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='机构标签'),
        ),
    ]