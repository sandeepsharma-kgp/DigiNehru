# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-03 13:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='menu_item',
            new_name='food_item',
        ),
    ]
