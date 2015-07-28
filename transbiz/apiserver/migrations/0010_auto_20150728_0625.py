# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0009_auto_20150728_0607'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sale',
            options={'verbose_name': 'Sale', 'verbose_name_plural': 'Sales'},
        ),
        migrations.AlterField(
            model_name='sale',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2015, 8, 4, 6, 25, 34, 904603, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sale',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now, validators=[django.core.validators.MinValueValidator(django.utils.timezone.now)]),
        ),
    ]
