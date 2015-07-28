# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0011_auto_20150728_0625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2015, 8, 4, 6, 46, 35, 121576, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sale',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2015, 7, 28, 6, 46, 35, 121519, tzinfo=utc), validators=[django.core.validators.MinValueValidator(datetime.datetime(2015, 7, 28, 6, 46, 35, 121536, tzinfo=utc))]),
        ),
    ]
