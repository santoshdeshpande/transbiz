# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import transbiz.apiserver.models


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0038_auto_20150803_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='end_date',
            field=models.DateTimeField(default=transbiz.apiserver.models.get_end_date),
        ),
        migrations.AlterField(
            model_name='sale',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
