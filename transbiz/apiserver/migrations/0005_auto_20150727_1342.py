# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0004_auto_20150724_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='company',
            field=models.ForeignKey(related_name='subscriptions', to='apiserver.Company'),
        ),
    ]
