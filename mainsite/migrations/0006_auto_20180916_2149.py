# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-09-16 21:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0005_auto_20180916_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordertime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
