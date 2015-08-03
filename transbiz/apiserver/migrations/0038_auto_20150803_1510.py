# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0037_auto_20150731_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pushnotification',
            name='gcm_id',
            field=models.CharField(max_length=400),
        ),
    ]
