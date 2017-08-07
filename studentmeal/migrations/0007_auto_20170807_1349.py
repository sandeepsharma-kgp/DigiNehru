# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 13:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_auto_20170712_1007'),
        ('studentmeal', '0006_eating_meals_opted'),
    ]

    operations = [
        migrations.CreateModel(
            name='mealcount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eating_on', models.DateField()),
                ('meals_taken', multiselectfield.db.fields.MultiSelectField(choices=[(0, b'Breakfast'), (1, b'Lunch'), (2, b'Snacks'), (3, b'Dinner')], default=[], max_length=7)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Students')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='mealcount',
            unique_together=set([('student', 'eating_on')]),
        ),
    ]