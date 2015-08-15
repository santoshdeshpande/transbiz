# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0044_auto_20150815_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
