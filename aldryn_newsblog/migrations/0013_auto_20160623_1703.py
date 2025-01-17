# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-23 21:03

from django.db import migrations, models

import app_data.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0012_auto_20160503_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsblogarchiveplugin',
            name='cache_duration',
            field=models.PositiveSmallIntegerField(default=0, help_text="The maximum duration (in seconds) that this plugin's contentshould be cached. Values between 5 minutes (300) and one day (84600) recommended)."),
        ),
        migrations.AddField(
            model_name='newsbloglatestarticlesplugin',
            name='cache_duration',
            field=models.PositiveSmallIntegerField(default=0, help_text="The maximum duration (in seconds) that this plugin's contentshould be cached. Values between 5 minutes (300) and one day (84600) recommended)."),
        ),
        migrations.AddField(
            model_name='newsblogrelatedplugin',
            name='cache_duration',
            field=models.PositiveSmallIntegerField(default=0, help_text="The maximum duration (in seconds) that this plugin's contentshould be cached. Values between 5 minutes (300) and one day (84600) recommended)."),
        ),
        migrations.AlterField(
            model_name='newsblogconfig',
            name='app_data',
            field=app_data.fields.AppDataField(default='{}', editable=False),
        ),
    ]
