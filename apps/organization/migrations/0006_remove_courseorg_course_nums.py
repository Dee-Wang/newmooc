# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-10 15:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_auto_20170505_1120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseorg',
            name='course_nums',
        ),
    ]