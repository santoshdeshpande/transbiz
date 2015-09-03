# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('apiserver', '0050_auto_20150831_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyrequest',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='buyresponse',
            name='is_deal',
            field=models.BooleanField(default=False),
        ),
    ]
