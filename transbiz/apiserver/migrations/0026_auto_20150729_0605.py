# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0025_auto_20150729_0526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pushnotification',
            name='app_version',
            field=models.DecimalField(verbose_name=b'Application Version', max_digits=4, decimal_places=2, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
    ]
