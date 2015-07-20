# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0008_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='established_year',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1950)]),
        ),
        migrations.AddField(
            model_name='company',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
