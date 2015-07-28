# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import transbiz.apiserver.models


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0019_auto_20150728_0705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='end_date',
            field=models.DateField(default=transbiz.apiserver.models.get_end_date),
        ),
        migrations.AlterField(
            model_name='sale',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
