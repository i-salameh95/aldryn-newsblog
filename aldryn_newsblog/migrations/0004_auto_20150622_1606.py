# -*- coding: utf-8 -*-

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0003_auto_20150422_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsblogconfig',
            name='template_prefix',
            field=models.CharField(max_length=20, null=True, verbose_name='Prefix for template dirs', blank=True),
            preserve_default=True,
        ),
    ]
