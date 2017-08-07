# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-06 18:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentmeal', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='eating',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='eating',
            name='student',
        ),
        migrations.DeleteModel(
            name='eating',
        ),
    ]