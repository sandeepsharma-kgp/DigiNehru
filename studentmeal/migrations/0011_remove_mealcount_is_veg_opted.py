# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-15 17:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentmeal', '0010_mealcount_is_veg_opted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mealcount',
            name='is_veg_opted',
        ),
    ]