# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0035_auto_20150731_0508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleresponse',
            name='cities',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), size=None),
        ),
    ]
