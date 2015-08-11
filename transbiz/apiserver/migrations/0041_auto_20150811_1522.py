# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0040_auto_20150811_1312'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
    ]
