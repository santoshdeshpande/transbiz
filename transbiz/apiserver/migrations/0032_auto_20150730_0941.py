# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0031_saleresponse'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='saleresponse',
            options={'verbose_name': 'Sale Response', 'verbose_name_plural': 'Sale Responses'},
        ),
    ]
