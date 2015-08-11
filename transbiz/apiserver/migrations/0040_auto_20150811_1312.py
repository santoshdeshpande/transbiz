# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0039_auto_20150810_1444'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'default_permissions': (), 'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
    ]
