# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0050_auto_20150826_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyrequest',
            name='delivery_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
