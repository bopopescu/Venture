# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-03-07 08:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venturelift_profiles', '0004_auto_20200222_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='about',
            field=models.TextField(help_text='Briefly describe your self', null=True),
        ),
    ]
