# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-20 18:02
from __future__ import unicode_literals

from django.db import migrations
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('studentmeal', '0007_auto_20170807_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='mealcount',
            name='vn',
            field=django_mysql.models.JSONField(default=dict),
        ),
    ]
