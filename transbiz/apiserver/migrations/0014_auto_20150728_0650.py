# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0013_auto_20150728_0646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2015, 8, 4, 6, 50, 56, 117172, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sale',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2015, 7, 28, 6, 50, 56, 117131, tzinfo=utc)),
        ),
    ]
