# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-12 10:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_students_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='profile',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
    ]