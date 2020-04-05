# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-02-22 14:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venturelift_profiles', '0003_auto_20200222_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supporterprofile',
            name='interest_sectors',
        ),
        migrations.AddField(
            model_name='supporterprofile',
            name='interest_sectors',
            field=models.ManyToManyField(blank=True, help_text='Target Sectors', null=True, to='venturelift_profiles.BusinessCategory'),
        ),
    ]
