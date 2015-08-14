# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0042_saleresponse_requested_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleresponse',
            name='questions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200, blank=True), size=None),
        ),
    ]
