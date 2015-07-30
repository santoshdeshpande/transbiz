# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0032_auto_20150730_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleresponse',
            name='cities',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), size=20),
        ),
        migrations.AlterField(
            model_name='saleresponse',
            name='questions',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50, blank=True), size=1), size=10),
        ),
    ]
